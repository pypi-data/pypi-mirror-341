from rich.segment import Segment

from ..core.box import Box
from ..core.versioned import Versioned, changes


class Buffer(Versioned):
    """
    A 2D sparse grid of rich.Segment objects.
    """

    def __init__(self):
        """
        Initialize the buffer as a sparse structure.
        """
        super().__init__()
        self._data = {}  # {y: {x: segment}}
        self.box = Box()
        self._size = 0

    def __getitem__(self, coords):
        """
        Get the item at the given coordinates.

        Args:
            coords: A tuple of (x, y) coordinates

        Returns:
            The Segment at those coordinates or None if empty
        """
        x, y = coords
        return self._data.get(y, {}).get(x)

    @changes
    def __setitem__(self, coords, segment):
        """
        Set a segment at the given coordinates.

        Args:
            coords: A tuple of (x, y) coordinates
            segment: The Segment to place at these coordinates
        """
        x, y = coords
        self.set(x, y, segment)

    @changes
    def __iadd__(self, other) -> "Buffer":
        """
        Merge another buffer into this one.
        """
        if not isinstance(other, Buffer):
            raise TypeError(f"Cannot merge {type(other)} with Buffer")

        # Update box in one operation
        self.box += other.box

        # Merge the data from the other buffer
        for y, row in other._data.items():
            if y not in self._data:
                # Fast path: copy entire row if it doesn't exist in current buffer
                self._data[y] = row.copy()
            else:
                # Update existing row
                self._data[y].update(row)

        self.recalculate(box=False)

        return self

    def __add__(self, other) -> "Buffer":
        """
        Create a new buffer by merging this buffer with another.
        """
        result = self.copy()
        result += other
        return result

    def __and__(self, box: Box) -> "Buffer":
        """
        Crop the buffer to the given box.
        Returns a newly allocated buffer.
        """
        result = Buffer()
        for y in range(box.min_y, box.max_y):
            row = self._data.get(y)
            if not row:
                continue
            for x in range(box.min_x, box.max_x):
                if x in row:
                    result.set(x, y, row[x])
        return result

    @changes
    def __iand__(self, box: Box) -> "Buffer":
        """
        Crop the buffer to the given box.
        This modifies the buffer in place.
        """
        self._data = (self & box)._data
        self.box = box
        self.recalculate(box=False)

        return self

    def __sub__(self, other: "Buffer") -> "Buffer":
        """
        Create a new buffer representing the difference: self - other.
        Only includes cells in self that differ from other.
        """
        delta = Buffer()
        for y, row in self._data.items():
            for x, seg in row.items():
                if seg != other[x, y]:
                    delta.set(x, y, seg)
        return delta

    @changes
    def __isub__(self, other: "Buffer") -> "Buffer":
        """
        Remove from self any cells that are identical in other.
        Modifies the buffer in-place.
        """
        for y in list(self._data.keys()):
            row = self._data[y]
            for x in list(row.keys()):
                if self[x, y] == other[x, y]:
                    del row[x]
            if not row:
                del self._data[y]

        self.recalculate()
        return self

    def __len__(self):
        """
        Get the number of cells set in the buffer.
        """
        return self._size

    @changes
    def set(self, x, y, segment):
        """
        Set cell(s) starting at given coordinates with a Segment.
        Handles multi-character segments by writing each character in sequence.

        Args:
            x: Starting X coordinate
            y: Y coordinate
            segment: Rich Segment object to place at this position
        """

        self.box.update(x, y)
        txtlen = len(segment.text)
        if txtlen > 1:
            self.box.update(x - 1 + txtlen, y)

        # Ensure y entry exists before loop
        if not self._data.get(y):
            self._data[y] = {}

        # Handle multi-character segments by writing each char
        style = segment.style
        for i, char in enumerate(segment.text):
            if x + i not in self._data[y]:
                self._size += 1
            # Store a new single-character segment
            self._data[y][x + i] = Segment(char, style)

    def copy(self):
        """
        Create a deep copy of this buffer.

        Returns:
            A new Buffer instance with the same content
        """
        new_buffer = Buffer()

        # Copy the box
        new_buffer.box = Box(
            self.box.min_x, self.box.min_y, self.box.max_x, self.box.max_y
        )

        # Copy the data structure
        for y, row in self._data.items():
            new_buffer._data[y] = row.copy()

        return new_buffer

    @changes
    def recalculate(self, size: bool = True, box: bool = True):
        """
        Recalculate the size and box
        """
        if size:
            self._size = sum(len(row) for row in self._data.values())

        if box:
            self.box.reset()
            for y, row in self._data.items():
                for x in row:
                    self.box.update(x, y)
