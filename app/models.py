# app/models.py

from app import db
from sqlalchemy.dialects.postgresql import insert as pg_insert
import pandas as pd
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.sql import func
import datetime
import re

DELTA_TYPES = ["pct", "abs"]
DEFAULT_DELTA_TYPE = "pct"
CODE_MAX_LEN = 12
TIME_FREQUENCIES = ["DA", "D", "W", "M", "B", "Q", "S", "Y"]


def validate_code_len(_validate_code):
    def wrapper(*args, **kwargs):
        code = _validate_code(*args, **kwargs)
        if isinstance(code, str):
            if len(code) > CODE_MAX_LEN:
                raise ValueError(f"Code must be {CODE_MAX_LEN} characters or less.")
        return code

    return wrapper


# Association table for many-to-many relationship between SeriesGroup and SeriesBase
seriesgroup_seriesbase = db.Table(
    "seriesgroup_seriesbase",
    db.Column(
        "seriesgroup_id", db.Integer, db.ForeignKey("series_group.id"), primary_key=True
    ),
    db.Column(
        "seriesbase_id", db.Integer, db.ForeignKey("series_base.id"), primary_key=True
    ),
)

# Association table for many-to-many relationship between SeriesBase and Keyword
seriesbase_keyword = db.Table(
    "seriesbase_keyword",
    db.Column(
        "seriesbase_id", db.Integer, db.ForeignKey("series_base.id"), primary_key=True
    ),
    db.Column("keyword_id", db.Integer, db.ForeignKey("keyword.id"), primary_key=True),
)


class BaseModel(db.Model):
    __abstract__ = True

    def save(self, session=None, commit=True):
        """
        Saves the current instance to the database, ensuring any dependent objects are also saved.
        session (db.session): The SQLAlchemy session to use. If None, uses db.session.
        commit (bool): Whether or not to commit immediately.
        """
        if session is None:
            session = db.session

        self._save_dependencies(session)

        session.add(self)

        if commit:
            session.commit()

        # Flush to ensure the instance is bound to the session
        session.flush()

        # Handle pending keywords if any
        if hasattr(self, "_pending_keywords"):
            for kw in self._pending_keywords:
                self.add_keyword(kw, session=session)
            del self._pending_keywords  # Clear pending keywords

    def _save_dependencies(self, session):
        """
        Override this in child classes to save any dependencies (parents or children).
        Default implementation does nothing.
        """
        pass


class Keyword(BaseModel):
    __tablename__ = "keyword"
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # Relationship to SeriesBase
    series = db.relationship(
        "SeriesBase",
        secondary=seriesbase_keyword,
        back_populates="keywords",
        lazy="select",
    )

    def __repr__(self):
        return f"<Keyword {self.word}>"


class SeriesBase(BaseModel):
    __tablename__ = "series_base"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    type = db.Column(db.String(50))  # Discriminator column

    date_create = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    date_update = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    keywords = db.relationship(
        "Keyword",
        secondary=seriesbase_keyword,
        back_populates="series",
        lazy="select",  # Changed from 'dynamic' to 'select'
    )

    def __init__(self, name, description=None, keywords=None, **kwargs):
        """
        Initializes a SeriesBase instance.

        Parameters:
        - name (str): The name of the series.
        - description (str, optional): A description of the series.
        - keywords (list of str, optional): A list of keyword strings to associate with the series.
        - **kwargs: Additional keyword arguments for other fields.
        """
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        if keywords:
            self._pending_keywords = keywords.copy()  # Store pending keywords
        else:
            self._pending_keywords = []

    __mapper_args__ = {
        "polymorphic_identity": "series_base",
        "polymorphic_on": type,
        "with_polymorphic": "*",
    }

    def __repr__(self):
        return f"<SeriesBase {self.name}>"

    def add_keyword(self, keyword_word, session=None):
        """
        Adds a keyword to the series. Creates the keyword if it doesn't exist.

        Parameters:
        - keyword_word (str): The keyword string to add.
        - session (Session, optional): The SQLAlchemy session to use. Defaults to db.session.
        """
        if isinstance(keyword_word, (list, tuple)):
            for kw in keyword_word:
                self.add_keyword(kw, session=session)
            return

        if not isinstance(keyword_word, str):
            raise TypeError("Keyword must be a string.")
        if len(keyword_word) > 50:
            raise ValueError("Keyword must be 50 characters or less.")

        if session is None:
            session = db.session

        keyword = session.query(Keyword).filter_by(word=keyword_word).first()
        if not keyword:
            keyword = Keyword(word=keyword_word)
            session.add(keyword)
        if keyword not in self.keywords:
            self.keywords.append(keyword)

    def remove_keyword(self, keyword_word):
        """
        Removes a keyword from the series.

        Parameters:
        - keyword_word (str): The keyword string to remove.
        """
        keyword = Keyword.query.filter_by(word=keyword_word).first()
        if keyword and keyword in self.keywords:
            self.keywords.remove(keyword)

    @staticmethod
    @validate_code_len
    def _validate_code(code, class_code):
        if class_code is not None and code is not None:
            if class_code == code:
                return class_code
            else:
                raise ValueError(
                    "Only Code or the code specified by the class must be passed. "
                    + "'code' is the same as the class code, but it aims to facilitate instantiation."
                )
        elif class_code is not None:
            return class_code
        elif code is not None:
            return code
        else:
            raise ValueError(
                "Either code or class code ('time_series_code' or 'series_group_code') must be provided."
            )

    @staticmethod
    def _validate_delta_type(delta_type):
        if delta_type is None:
            return DEFAULT_DELTA_TYPE
        if delta_type.lower() not in DELTA_TYPES:
            raise ValueError(
                "delta_type must be one of the following: " + ", ".join(DELTA_TYPES)
            )
        return delta_type.lower()

    @staticmethod
    def _validate_description(description):
        if description is not None and not isinstance(description, str):
            raise ValueError("Description must be a string or None.")
        return description

    @staticmethod
    def _validate_time_frequency(time_frequency):
        if time_frequency is not None and time_frequency not in TIME_FREQUENCIES:
            raise ValueError(
                "Time frequency must be one of the following: "
                + ", ".join(TIME_FREQUENCIES)
            )
        return time_frequency


class SeriesGroup(SeriesBase):
    __tablename__ = "series_group"
    id = db.Column(db.Integer, db.ForeignKey("series_base.id"), primary_key=True)
    series_group_code = db.Column(
        db.String(CODE_MAX_LEN), nullable=False, unique=True
    )  # Renamed and kept unique

    def __init__(
        self,
        name,
        description=None,
        series_group_code=None,
        code=None,
        keywords=None,
        **kwargs,
    ):
        """
        Initializes a SeriesGroup instance.

        Parameters:
        - name (str): The name of the series group.
        - description (str, optional): A description of the series group.
        - series_group_code (str): A unique code for the series group.
        - keywords (list of str, optional): A list of keyword strings to associate with the series group.
        - **kwargs: Additional keyword arguments for other fields.
        """
        super().__init__(name, description=description, keywords=keywords, **kwargs)
        self.series_group_code = self._validate_code(code, series_group_code)

    # Self-referential relationship for nested SeriesGroups
    parent_id = db.Column(db.Integer, db.ForeignKey("series_group.id"), nullable=True)
    children = db.relationship(
        "SeriesGroup",
        backref=db.backref("parent", remote_side=[id]),
        lazy="dynamic",
        foreign_keys=[parent_id],  # Explicitly specify foreign_keys
    )

    # Many-to-many relationship with SeriesBase (TimeSeries and SeriesGroup)
    series = db.relationship(
        "SeriesBase",
        secondary=seriesgroup_seriesbase,
        backref=db.backref("series_groups", lazy="dynamic"),
        lazy="dynamic",
    )

    __mapper_args__ = {
        "polymorphic_identity": "series_group",
    }

    def __repr__(self):
        return (
            f"SeriesGroup(name={self.name}, code={self.time_series_code}, "
            + f"n_children={self.series.count()})"
        )


class TimeSeries(SeriesBase):
    __tablename__ = "time_series"
    id = db.Column(db.Integer, db.ForeignKey("series_base.id"), primary_key=True)
    time_series_code = db.Column(db.String(CODE_MAX_LEN), nullable=False, unique=True)
    type_id = db.Column(db.Integer, db.ForeignKey("time_series_type.id"), nullable=True)
    time_frequency = db.Column(db.String(3), nullable=True, default="M")
    delta_type = db.Column(db.String(10), nullable=True, default="pct")

    # The main fix is here in save()
    def save(
        self,
        allow_update=True,
        keep_old_description=True,
        keep_old_delta_type=True,
        keep_old_time_frequency=False,
        join_keywords=True,
        join_data_points=True,
        session=None,
        commit=True,
    ):
        """
        Saves the TimeSeries instance to the database. If a conflict on
        name or code is found and allow_update=True, it merges data
        into the *existing* record in place (no deletion, no reuse of old IDs).

        Parameters:
            allow_update (bool): Whether to allow merging with an existing TimeSeries.
            keep_old_description (bool): Retain the old description if merging.
            keep_old_delta_type (bool): Retain the old delta_type if merging.
            keep_old_time_frequency (bool): Retain the old time_frequency if merging.
            join_keywords (bool): Merge keywords when updating.
            join_data_points (bool): Merge data points when updating.
            session (Session): Optional SQLAlchemy session. Defaults to db.session.
            commit (bool): Commit the transaction after saving if True.
        """
        from sqlalchemy.exc import IntegrityError, InvalidRequestError
        from app import db

        if session is None:
            session = db.session

        try:  # Ensure all pending objects are persisted
            # 1) Check for existing conflicts by name or code.
            time_series_with_same_name = (
                session.query(TimeSeries).filter_by(name=self.name).first()
            )
            time_series_with_same_code = (
                session.query(TimeSeries)
                .filter_by(time_series_code=self.time_series_code)
                .first()
            )

            if time_series_with_same_name or time_series_with_same_code:
                # 2) If we do NOT allow updates, raise an immediate ValueError
                if not allow_update:
                    if time_series_with_same_name and time_series_with_same_code:
                        raise ValueError(
                            "TimeSeries with the same name and code already exists."
                        )
                    elif time_series_with_same_name:
                        raise ValueError(
                            "TimeSeries with the same name already exists."
                        )
                    elif time_series_with_same_code:
                        raise ValueError(
                            "TimeSeries with the same code already exists."
                        )
                else:
                    # 3) Merge logic in-place:
                    #    old_ts is the record we will update rather than deleting it.
                    if time_series_with_same_name and time_series_with_same_code:
                        # If both exist, ensure they refer to the *same* instance
                        if time_series_with_same_name != time_series_with_same_code:
                            raise ValueError(
                                "One TimeSeries has the same name and another the same code. Change one of them."
                            )
                    old_ts = time_series_with_same_name or time_series_with_same_code

                    # Update fields on the *existing* old_ts in place.
                    if not keep_old_description:
                        old_ts.description = self.description
                    if not keep_old_delta_type:
                        old_ts.delta_type = self.delta_type
                    if not keep_old_time_frequency:
                        if self.time_frequency:
                            old_ts.time_frequency = self.time_frequency
                    else:
                        # keep old, unless we had no time_frequency on self
                        if old_ts.time_frequency is None and self.time_frequency:
                            old_ts.time_frequency = self.time_frequency

                    # Merge keywords if requested
                    if join_keywords and self.keywords:
                        old_ts.join_keywords(self.keywords, session=session)

                    # Merge data points if requested
                    if join_data_points and self.data_points:
                        old_ts.join_data_points(self.data_points, session=session)

                    # Mark the old record as updated
                    old_ts.date_update = func.now()

                    # Reflect the final state from old_ts back into self,
                    # so 'self' remains consistent in Python memory.
                    self.id = old_ts.id
                    self.date_create = old_ts.date_create
                    self.date_update = old_ts.date_update
                    self.description = old_ts.description
                    self.delta_type = old_ts.delta_type
                    self.time_frequency = old_ts.time_frequency
                    # Keywords, data points, etc., are also effectively on old_ts,
                    # so self.keywords, self.data_points are overshadowed by old_ts.

                    # Return now, because the "old_ts" is the real record in the DB
                    # We do NOT do "super().save()" on self, because old_ts is already
                    # persisted. We only commit if user wants to.
                    if commit:
                        session.commit()
                    return

            # 4) If there is no conflict or no update,
            #    proceed to a normal "new record" save.
            super().save(session=session, commit=commit)

        except ValueError:
            # Let your tests catch the ValueError directly if needed
            raise

        except IntegrityError as e:
            session.rollback()
            raise IntegrityError(
                f"Database integrity error while saving TimeSeries '{self.name}': {e}",
                e.params,
                e.orig,
            ) from e

        except InvalidRequestError as e:
            session.rollback()
            raise InvalidRequestError(
                f"Session conflict or invalid request while saving TimeSeries '{self.name}': {e}"
            ) from e

    def join_data_points(self, new_data_points, session=None):
        """
        Wrapper that calls upsert_data_points with commit=False by default.
        """
        self.upsert_data_points(new_data_points, session=session, commit=False)

    def join_keywords(self, new_keywords, session=None):
        """
        Ensures no duplicate Keywords are added.
        Accepts either Keyword objects or strings.
        """
        if session is None:
            session = db.session

        if not isinstance(new_keywords, list):
            raise TypeError(
                "new_keywords must be a list of Keyword objects or strings."
            )

        for kw in new_keywords:
            if isinstance(kw, Keyword):
                keyword = kw
            elif isinstance(kw, str):
                keyword = session.query(Keyword).filter_by(word=kw).first()
                if not keyword:
                    keyword = Keyword(word=kw)
                    session.add(keyword)
            else:
                raise TypeError("Keywords must be instances of Keyword or str.")

            if keyword not in self.keywords:
                self.keywords.append(keyword)

    def _save_dependencies(self, session):
        """
        Save the related TimeSeriesType and DataPoints, if they're not already.
        Avoid re-adding objects attached to a different session.
        """
        if self.time_series_type:
            # see if it's in a different session
            tstype_state = db.inspect(self.time_series_type)
            if tstype_state.session is None:
                # not attached to any session yet
                session.add(self.time_series_type)
            elif tstype_state.session != session:
                # attached to a different session
                self.time_series_type = session.merge(self.time_series_type)

        # Save child DataPoints if they're new or in another session
        for dp in self.data_points:
            dp_state = db.inspect(dp)
            if dp_state.session is None:
                session.add(dp)
            elif dp_state.session != session:
                # rarely needed, but if your DataPoints are also from a different session
                dp = session.merge(dp)

    @property
    def number_data_points(self):
        try:
            return len(self.data_points)
        except TypeError:
            return 0

    def __repr__(self):
        return (
            f"TimeSeries(name={self.name}, code={self.time_series_code}, "
            + f"len={self.number_data_points}, freq={self.time_frequency}, delta={self.delta_type})"
        )

    data_points = db.relationship(
        "DataPoint", backref="time_series", lazy=True, cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_identity": "time_series",
    }

    def __init__(
        self,
        name,
        code=None,
        time_series_code=None,
        type_id=None,
        time_frequency=None,
        delta_type=None,
        **kwargs,
    ):
        super().__init__(name, **kwargs)
        self.time_series_code = self._validate_code(code, time_series_code)
        self.type_id = type_id
        self.time_frequency = time_frequency
        self.delta_type = self._validate_delta_type(delta_type)

    def to_dataframe(
        self,
        only_most_recent_per_date=True,
        filter_date_release_smaller_or_equal_to=None,
        include_date_release=False,
        include_date_create=False,
    ):
        """
        Returns the TimeSeries data as a pandas DataFrame.
        """
        data = {
            "date": [dp.date for dp in self.data_points],
            "value": [dp.value for dp in self.data_points],
            "date_create": [dp.date_create for dp in self.data_points],
            "date_release": [dp.date_release for dp in self.data_points],
        }
        ts_dataframe = pd.DataFrame(data).sort_values(
            ["date", "date_release", "date_create"]
        )
        if only_most_recent_per_date:
            ts_dataframe = ts_dataframe.drop_duplicates(subset=["date"])
        ts_dataframe = ts_dataframe.set_index("date").rename(
            {"value": self.name}, axis=1
        )
        if filter_date_release_smaller_or_equal_to is not None:
            if isinstance(filter_date_release_smaller_or_equal_to, str):
                try:
                    filter_date = pd.to_datetime(
                        filter_date_release_smaller_or_equal_to
                    )
                except ValueError:
                    raise ValueError(
                        "filter_date_release_smaller_or_equal_to must be a valid date string."
                    )
            elif not isinstance(
                filter_date_release_smaller_or_equal_to,
                (datetime.datetime, datetime.date),
            ):
                raise ValueError(
                    "filter_date_release_smaller_or_equal_to must be a valid date string."
                )
            else:
                filter_date = filter_date_release_smaller_or_equal_to
            ts_dataframe = ts_dataframe[ts_dataframe["date_release"] <= filter_date]

        if not include_date_release:
            ts_dataframe = ts_dataframe.drop(columns=["date_release"])
        if not include_date_create:
            ts_dataframe = ts_dataframe.drop(columns=["date_create"])
        return ts_dataframe

    @classmethod
    def from_dataframe(
        cls,
        df,
        series_groups=None,
        time_series_type=None,
        name=None,
        code=None,
        time_frequency=None,
        delta_type=None,
        description=None,
        date_column=None,
        all_columns_have_same_series_groups=False,
    ):
        """
        Creates one or more TimeSeries objects from a pandas DataFrame without saving to the database.

        Returns
        -------
        TimeSeries or List[TimeSeries]
            A single TimeSeries if exactly one column is processed, or a list of multiple TimeSeries objects.
        """
        if date_column is not None:
            if date_column not in df.columns:
                raise ValueError(f"Date column '{date_column}' not found in DataFrame.")
            df = df.set_index(date_column)

        if "date" in [c.lower() for c in df.columns.tolist()]:
            df = df.set_index("date")
        try:
            df.index = pd.to_datetime(df.index)
        except ValueError:
            raise ValueError(
                "The DataFrame must have a datetime index or specify a date_column."
            )
        df.index.name = "date"

        if len(df.columns) == 1:
            if name is None:
                name = df.columns[0]

            if isinstance(time_frequency, (list, tuple)):
                if len(time_frequency) != 1:
                    raise ValueError(
                        "Time frequency list must match the number of columns in the DataFrame."
                    )
                time_frequency = time_frequency[0]
            if isinstance(time_frequency, str):
                if time_frequency not in TIME_FREQUENCIES:
                    raise ValueError(
                        "Time frequency must be one of the following: "
                        + ", ".join(TIME_FREQUENCIES)
                    )

            if code is None:
                raise ValueError("Code must be provided for each column passed.")
            elif isinstance(code, (list, tuple)):
                if len(code) != 1:
                    raise ValueError(
                        "Code list must match the number of columns in the DataFrame."
                    )
                code = code[0]
            elif not isinstance(code, str):
                raise ValueError(
                    "Code must be provided as string or as a list/tuple with len=1."
                )

            if isinstance(time_series_type, (list, tuple)):
                if len(time_series_type) != 1:
                    raise ValueError(
                        "TimeSeriesType list must match the number of columns in the DataFrame."
                    )
                time_series_type = time_series_type[0]
            if (
                not isinstance(time_series_type, (str, TimeSeriesType))
                and time_series_type is not None
            ):
                raise ValueError(
                    "TimeSeriesType must be provided as string, None or a list/tuple with len=1."
                )

            if isinstance(delta_type, (list, tuple)):
                if len(delta_type) != 1:
                    raise ValueError(
                        "Delta type list must match the number of columns in the DataFrame."
                    )
                delta_type = delta_type[0]
            if not isinstance(delta_type, str) and delta_type is not None:
                raise ValueError(
                    "Delta type must be provided as string, None or a list/tuple with len=1."
                )
            elif isinstance(delta_type, str):
                delta_type = delta_type.lower()
                if delta_type not in DELTA_TYPES:
                    raise ValueError(
                        "Delta type must be one of the following: "
                        + ", ".join(DELTA_TYPES)
                    )

            return cls.build_time_series_object(
                df.iloc[:, 0].values,
                df.index,
                name,
                code,
                time_frequency,
                delta_type,
                series_groups,  # Can be None
                TimeSeriesType._convert_to_time_series_type(time_series_type),
                description,
            )
        else:
            if name is None:
                name = list(df.columns)
            elif isinstance(name, tuple):
                name = list(name)
            elif name and not isinstance(name, list):
                raise ValueError(
                    "Name must be a list if multiple columns are provided."
                )
            elif len(name) != len(df.columns):
                raise ValueError(
                    "Name list must match the number of columns in the DataFrame."
                )

            if isinstance(time_frequency, (list, tuple)):
                if len(time_frequency) != len(df.columns):
                    raise ValueError(
                        "Time frequency list must match the number of columns in the DataFrame or be equal for all."
                    )
                if not all([tf in TIME_FREQUENCIES for tf in time_frequency]):
                    raise ValueError(
                        "Time frequency must be one of the following: "
                        + ", ".join(TIME_FREQUENCIES)
                    )
            elif isinstance(time_frequency, str) or time_frequency is None:
                if (
                    time_frequency not in TIME_FREQUENCIES
                    and time_frequency is not None
                ):
                    raise ValueError(
                        "Time frequency must be one of the following: "
                        + ", ".join(TIME_FREQUENCIES)
                    )
                time_frequency = [time_frequency] * len(df.columns)
            elif time_frequency is not None:
                raise ValueError(
                    "Time frequency must be a string or a list of strings."
                )

            if isinstance(time_series_type, (list, tuple)):
                if len(time_series_type) != len(df.columns):
                    raise ValueError(
                        "TimeSeriesType list must match the number of columns in the DataFrame."
                    )
                if not all(
                    [
                        isinstance(tst, (TimeSeriesType, str)) or tst is None
                        for tst in time_series_type
                    ]
                ):
                    raise ValueError(
                        "TimeSeriesType must be an instance of TimeSeriesType or string."
                    )
            elif (
                isinstance(time_series_type, (TimeSeriesType, str))
                or time_series_type is None
            ):
                time_series_type = [time_series_type] * len(df.columns)
            elif time_series_type is not None:
                raise ValueError(
                    "TimeSeriesType must be an instance of TimeSeriesType, string, or a list of strings."
                )

            if isinstance(delta_type, (list, tuple)):
                if len(delta_type) != len(df.columns):
                    raise ValueError(
                        "Delta type list must match the number of columns in the DataFrame."
                    )
                if not all([dt in DELTA_TYPES for dt in delta_type]):
                    raise ValueError(
                        "Delta type must be one of the following: "
                        + ", ".join(DELTA_TYPES)
                    )
            elif isinstance(delta_type, str) or delta_type is None:
                if isinstance(delta_type, str):
                    delta_type = delta_type.lower()
                if delta_type not in DELTA_TYPES and delta_type is not None:
                    raise ValueError(
                        "Delta type must be one of the following: "
                        + ", ".join(DELTA_TYPES)
                    )
                delta_type = [delta_type] * len(df.columns)

            if code is None or not isinstance(code, (list, tuple)):
                raise ValueError(
                    "Code must be provided for each column as a list or tuple passed."
                )
            elif len(code) != len(df.columns):
                raise ValueError(
                    "Code list must match the number of columns in the DataFrame."
                )

            if isinstance(description, str):
                description = [description] * len(df.columns)
            elif isinstance(description, (list, tuple)):
                description = (
                    list(description) if isinstance(description, tuple) else description
                )
                if len(description) != len(df.columns):
                    raise ValueError(
                        "Description list must match the number of columns in the DataFrame."
                    )
            elif description is None:
                description = [description] * len(df.columns)
            else:
                raise ValueError(
                    "Description must be a string, a list or None if multiple columns"
                )

            # Allow series_groups to be optional
            if series_groups is not None:
                if isinstance(series_groups, (str, int, SeriesGroup)):
                    series_groups = [series_groups] * len(df.columns)
                elif not isinstance(series_groups, list):
                    raise ValueError(
                        "SeriesGroups must be provided as list, string, or SeriesGroup instances"
                    )

                if len(series_groups) != len(df.columns):
                    if not all_columns_have_same_series_groups:
                        raise ValueError(
                            "SeriesGroups list must match the number of columns in the DataFrame or "
                            + "parameter 'all_columns_have_same_series_groups=True'."
                        )
            else:
                series_groups = [None] * len(df.columns)  # No groups associated

            if isinstance(description, str) and description is not None:
                raise ValueError(
                    "Description must be a list if multiple columns are provided."
                )

            if (
                not all([g is None for g in series_groups])
                and all_columns_have_same_series_groups
            ):
                all_columns_have_same_series_groups = True
                col_series_groups = series_groups
            else:
                all_columns_have_same_series_groups = False

            all_columns_have_same_series_groups = (
                False
                if all([g is None for g in series_groups])
                else all_columns_have_same_series_groups
            )

            all_time_series = []
            for i, col in enumerate(df.columns):
                if not all_columns_have_same_series_groups:
                    col_series_groups = series_groups[i]
                all_time_series.append(
                    cls.build_time_series_object(
                        df[col].values,
                        df.index,
                        name[i],
                        code[i],
                        time_frequency[i],
                        delta_type[i],
                        col_series_groups,
                        TimeSeriesType._convert_to_time_series_type(
                            time_series_type[i]
                        ),
                        description[i],
                    )
                )
            return all_time_series

    @classmethod
    def save_from_dataframe(
        cls,
        df,
        series_groups=None,
        time_series_type=None,
        name=None,
        description=None,
        date_column=None,
        value_columns=None,
    ):
        """
        Creates one or more TimeSeries objects from a pandas DataFrame and saves them to the database.

        Returns
        -------
        TimeSeries or List[TimeSeries]
            A single TimeSeries if exactly one column is processed, or a list of multiple TimeSeries objects.
        """
        time_series_objects = cls.from_dataframe(
            df,
            series_groups,
            time_series_type,
            name,
            description,
            date_column,
            value_columns,
        )
        if isinstance(time_series_objects, list):
            for ts in time_series_objects:
                ts.save()
        else:
            time_series_objects.save()
        return True

    @classmethod
    def build_time_series_object(
        cls,
        values,
        dates,
        time_series_name,
        time_series_code,
        time_frequency,
        delta_type,
        series_groups,
        time_series_type,
        description=None,
    ):
        """
        Build a TimeSeries object with DataPoint objects from provided values and dates.
        """
        cls._validate_description(description)
        cls._validate_time_frequency(time_frequency)
        cls._validate_delta_type(delta_type)

        data_points = []
        for i in range(len(values)):
            data_points.append(DataPoint(date=dates[i], value=values[i]))
        ts = cls(
            name=time_series_name,
            code=time_series_code,
            data_points=data_points,
        )
        if time_frequency is not None:
            ts.time_frequency = time_frequency
        if delta_type is not None:
            ts.delta_type = delta_type
        if description is not None:
            ts.description = description
        if isinstance(time_series_type, TimeSeriesType):
            ts.time_series_type = time_series_type
        else:
            ts.type_id = time_series_type

        # Associate with SeriesGroups if provided
        if series_groups:
            if isinstance(series_groups, SeriesGroup):
                ts.series_groups.append(series_groups)
            elif isinstance(series_groups, list):
                for sg in series_groups:
                    if sg is not None:
                        ts.series_groups.append(sg)
            else:
                raise ValueError(
                    "series_groups must be a SeriesGroup instance, list of SeriesGroup instances, or None"
                )

        return ts

    def upsert_data_points(self, new_data_points, session=None, commit=False):
        """
        Inserts new DataPoints in bulk with an "on conflict do nothing" upsert,
        so duplicate (time_series_id, date, value) rows are skipped.

        Parameters:
            new_data_points (list of DataPoint): The DataPoints to insert.
            session (Session, optional): The SQLAlchemy session to use.
                                         Defaults to db.session.
            commit (bool): Whether to commit the transaction after upsert.
        """
        if session is None:
            from app import db

            session = db.session

        # Ensure the TimeSeries itself is saved & has an ID
        if self.id is None:
            # This ensures self is in DB so we have a valid self.id
            # (Otherwise time_series_id can't be set properly.)
            self.save(session=session, commit=False)
            session.flush()  # Get a DB-generated ID for self

        # Build a list of dicts to insert
        data_rows = []
        for dp in new_data_points:
            # We only need the columns (time_series_id, date, value, date_release, etc.)
            data_rows.append(
                {
                    "time_series_id": self.id,
                    "date": dp.date,
                    "value": dp.value,
                    "date_release": dp.date_release,
                }
            )

        # If there's nothing to insert, just return
        if not data_rows:
            return

        # Build an INSERT statement for the data_point table
        stmt = pg_insert(DataPoint.__table__).values(data_rows)

        # "On conflict do nothing" will skip rows that violate the unique constraint
        # (time_series_id, date, value)
        stmt = stmt.on_conflict_do_nothing(
            index_elements=["time_series_id", "date", "value"]
        )

        # Execute the UPSERT in one bulk query
        session.execute(stmt)
        if commit:
            session.commit()

    @staticmethod
    def join_timeseries_to_dataframe(list_of_timeseries, how="outer"):
        """
        Joins multiple TimeSeries objects into a single DataFrame.
        """
        if isinstance(list_of_timeseries, tuple):
            list_of_timeseries = list(list_of_timeseries)
        if not isinstance(list_of_timeseries, list):
            raise ValueError("list_of_timeseries must be a list of TimeSeries objects.")
        if not all([isinstance(ts, TimeSeries) for ts in list_of_timeseries]):
            raise ValueError("list_of_timeseries must be a list of TimeSeries objects.")
        if how not in ["outer", "inner", "left", "right"]:
            raise ValueError("how must be one of 'outer', 'inner', 'left', 'right'.")

        # Start with the first TimeSeries
        df = list_of_timeseries[0].to_dataframe()

        # Join the rest
        for ts in list_of_timeseries[1:]:
            df = df.join(ts.to_dataframe(), how=how)

        return df

    def join_with_other_timeseries_to_dataframe(
        self, list_of_other_timeseries, how="outer"
    ):
        if isinstance(list_of_other_timeseries, tuple):
            list_of_other_timeseries = list(list_of_other_timeseries)
        elif isinstance(list_of_other_timeseries, TimeSeries):
            list_of_other_timeseries = [list_of_other_timeseries]
        if not isinstance(list_of_other_timeseries, list):
            raise ValueError(
                "list_of_other_timeseries must be a list of TimeSeries objects."
            )
        if not all([isinstance(ts, TimeSeries) for ts in list_of_other_timeseries]):
            raise ValueError(
                "list_of_other_timeseries must be a list of TimeSeries objects."
            )
        if how not in ["outer", "inner", "left", "right"]:
            raise ValueError("how must be one of 'outer', 'inner', 'left', 'right'.")

        return self.join_timeseries_to_dataframe(
            [self] + list_of_other_timeseries, how=how
        )

    @classmethod
    def save_all(
        cls,
        list_of_timeseries,
        allow_update=True,
        keep_old_description=True,
        keep_old_delta_type=True,
        keep_old_time_frequency=False,
        join_keywords=True,
        join_data_points=True,
        session=None,
        commit=True,
    ):
        if session is None:
            session = db.session

        if isinstance(list_of_timeseries, tuple):
            list_of_timeseries = list(list_of_timeseries)
        if not isinstance(list_of_timeseries, list):
            raise ValueError("list_of_timeseries must be a list of TimeSeries objects.")
        if not all([isinstance(ts, TimeSeries) for ts in list_of_timeseries]):
            raise ValueError("list_of_timeseries must be a list of TimeSeries objects.")

        for ts in list_of_timeseries:
            ts.save(
                allow_update,
                keep_old_description,
                keep_old_delta_type,
                keep_old_time_frequency,
                join_keywords,
                join_data_points,
                session,
                commit=False,
            )

        if commit:
            session.commit()

        return


class DataPoint(BaseModel):
    __tablename__ = "data_point"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Float, nullable=False)
    date_release = db.Column(db.Date, nullable=True)
    time_series_id = db.Column(
        db.Integer, db.ForeignKey("time_series.id"), nullable=False
    )

    date_create = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    date_update = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "time_series_id", "date", "value", name="uix_timeseries_date_value"
        ),
    )

    def __repr__(self):
        return f"DP({self.date}: {self.value})"

    def _save_dependencies(self, session):
        """
        Ensure the parent TimeSeries (and potentially its parent objects) are saved.
        """
        if self.time_series:
            # Make sure the parent TimeSeries saves its dependencies too.
            # This will also add the SeriesGroups and any other DataPoints.
            self.time_series._save_dependencies(session)
            session.add(self.time_series)


class TimeSeriesType(BaseModel):
    __tablename__ = "time_series_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(400))
    time_series = db.relationship("TimeSeries", backref="time_series_type", lazy=True)

    @classmethod
    def _convert_to_time_series_type(cls, tst):
        if tst is None:
            return tst
        elif isinstance(tst, cls):
            return tst
        elif isinstance(tst, str):
            tst = cls.query.filter_by(name=tst).first()
            if tst is not None:
                return tst
            else:
                return cls(name=tst)
        else:
            raise ValueError(
                "TimeSeriesType must be an instance of TimeSeriesType or a string."
            )

    date_create = db.Column(
        db.DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    date_update = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __mapper_args__ = {
        "polymorphic_identity": "time_series_type",
    }

    def __repr__(self):
        return f"TimeSeriesType(name={self.name})>"
