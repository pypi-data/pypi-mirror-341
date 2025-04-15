"""
Response wrapper classes for the Enemera API.
"""

from typing import List, TypeVar, Generic, Optional, Union, Type, Iterator, Sequence
import pathlib

from .data_utils import to_pandas, to_polars, to_csv, to_excel
from .models import BaseAPIModel

T = TypeVar('T', bound=BaseAPIModel)


class APIResponse(Generic[T]):
    """
    A wrapper around List[T] that adds data conversion methods while preserving
    the original list behavior.

    This class provides methods for converting API response data to various
    formats (pandas, polars, CSV, Excel) without changing the original list behavior.
    """

    def __init__(self, items: List[T], model_class: Type[T]):
        """
        Initialize the API response.

        Args:
            items: List of model instances
            model_class: The class of the model items
        """
        self._items = items
        self._model_class = model_class

    def __iter__(self) -> Iterator[T]:
        """Make the response iterable like a list."""
        return iter(self._items)

    def __getitem__(self, index):
        """Allow indexing like a list."""
        return self._items[index]

    def __len__(self) -> int:
        """Allow getting length like a list."""
        return len(self._items)

    def __repr__(self) -> str:
        """String representation."""
        return f"APIResponse({self._items!r})"

    # List compatibility methods
    def append(self, item: T) -> None:
        """Append an item to the list."""
        self._items.append(item)

    def extend(self, items: Sequence[T]) -> None:
        """Extend the list with more items."""
        self._items.extend(items)

    def to_pandas(self, index_col: Optional[str] = None):
        """
        Convert the response to a pandas DataFrame.

        Args:
            index_col: Column to use as index (optional)

        Returns:
            pandas.DataFrame: Pandas DataFrame representing the data
        """
        return to_pandas(self._items, index_col=index_col)

    def to_polars(self, index_col: Optional[str] = None):
        """
        Convert the response to a polars DataFrame.

        Args:
            index_col: Column to use as index (not used in polars, kept for API consistency)

        Returns:
            polars.DataFrame: Polars DataFrame representing the data
        """
        return to_polars(self._items, index_col=index_col)

    def to_csv(
            self,
            filepath: Union[str, pathlib.Path],
            index_col: Optional[str] = None,
            **csv_kwargs
    ):
        """
        Save the response to a CSV file.

        Args:
            filepath: Path to save the CSV file
            index_col: Column to use as index (optional)
            **csv_kwargs: Additional keyword arguments to pass to pandas.DataFrame.to_csv
        """
        to_csv(self._items, filepath, index_col=index_col, **csv_kwargs)

    def to_excel(
            self,
            filepath: Union[str, pathlib.Path],
            sheet_name: str = "Sheet1",
            index_col: Optional[str] = None,
            engine: str = "openpyxl",
            **excel_kwargs
    ):
        """
        Save the response to an Excel file.

        Args:
            filepath: Path to save the Excel file
            sheet_name: Name of the sheet to save the data to
            index_col: Column to use as index (optional)
            engine: Excel engine to use (default: openpyxl)
            **excel_kwargs: Additional keyword arguments to pass to pandas.DataFrame.to_excel
        """
        to_excel(
            self._items,
            filepath,
            sheet_name=sheet_name,
            index_col=index_col,
            engine=engine,
            **excel_kwargs
        )