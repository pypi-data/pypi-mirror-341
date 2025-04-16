from typing import Optional, Union, Tuple, TYPE_CHECKING

from pyglet.shapes import Circle as PygletCircle

from ..utils import Color
from .units import Unit, parse_width
from .window import get_window

if TYPE_CHECKING:
    from ..types import ColorType, UnitType
    from psychos.visual import Window

class Circle(PygletCircle):
    def __init__(
        self,
        position: Tuple[float, float] = (0, 0),
        radius: Optional[float] = None,
        color: Optional["ColorType"] = None,
        window: Optional["Window"] = None,
        coordinates: Optional[Union["UnitType", Unit]] = None,
        rotation: float = 0,
        **kwargs,
    ):
        """
        A circle shape that can be drawn on the screen.
        Parameters
        ----------
        position : Tuple[float, float], default=(0, 0)
            The position of the circle in the window.
        radius : Optional[float], default=None
            The radius of the circle, in the units of the window or the given coordinates.
        color : Optional[ColorType], default=None
            The color of the circle.
        window : Optional[Window], default=None
            The window in which the circle will be displayed.
        coordinates : Optional[Union[UnitType, Unit]], default=None
            The unit system to be used for positioning the circle.
        anchor_x : AnchorHorizontal, default="center"
            The horizontal anchor alignment of the circle.
        anchor_y : AnchorVertical, default="center"
            The vertical anchor alignment of the circle.
        rotation : float, default=0
            The rotation angle of the circle (in degrees 0–360).
        kwargs : dict
            Additional keyword arguments to pass to the Pyglet Circle.
        """
        # Retrieve window and set coordinate system
        self.window = window or get_window()
        self._coordinates = None
        self.coordinates = coordinates
        # Transform position according to coordinate system
        x, y = self.coordinates.transform(*position)
        # Radius parsing and fallback
        radius = parse_width(radius, window=self.window) or 1
        # Handle color parsing safely
        if color is None:
            rgba = (255, 255, 255, 255)
        else:
            rgba = Color(color).to_rgba255()
        # Initialize the base PygletCircle (expects RGB only)
        batch = kwargs.pop("batch", None)
        super().__init__(x, y, radius, color=rgba[:3], batch=batch, **kwargs)
        self._radius = radius
        self.rotation = rotation

    @property
    def coordinates(self) -> "Unit":
        """Get the coordinate system used for the circle."""
        return self._coordinates
    
    @coordinates.setter
    def coordinates(self, value: Optional[Union["UnitType", Unit]]):
        """Set the coordinate system used for the circle."""
        if value is None:
            self._coordinates = self.window.coordinates
        else:
            self._coordinates = Unit.from_name(value, window=self.window)


    @PygletCircle.color.setter
    def color(self, value: Optional[Union["ColorType", Color]]):
        """Set the color of the circle."""
        rgba = Color(value).to_rgba255() if value else (255, 255, 255, 255)
        PygletCircle.color.__set__(self, rgba[:3])

    @PygletCircle.radius.setter
    def radius(self, value: Optional[Union[str, int, float]]):
        value = parse_width(value, window=self.window)
        PygletCircle.radius.__set__(self, value)
        self._radius = value

    @property
    def position(self) -> Tuple[float, float]:
        """Get the position of the circle in pixels."""
        return self.x, self.y
    
    @position.setter
    def position(self, value: Tuple[float, float]):
        """Set the position of the circle using its coordinate system."""
        x, y = self.coordinates.transform(*value)
        self.x = x
        self.y = y
        
    def draw(self) -> "Circle":
        """Draw the circle and return itself."""
        super().draw()
        return self