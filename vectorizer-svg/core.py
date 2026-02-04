from math import sqrt

class Vector:
    def __init__(self, *coords):
        if len(coords) == 1 and hasattr(coords[0], "__iter__"):
            coords = tuple(coords[0])
        self.coords = tuple(float(c) for c in coords)
        if len(self.coords) == 0:
            raise ValueError("Vector must have at least one component.")

    def __len__(self):
        return len(self.coords)

    def __iter__(self):
        return iter(self.coords)

    def __repr__(self):
        return f"Vector{self.coords}"

    def __add__(self, other):
        other = self._coerce(other)
        return Vector(a + b for a, b in zip(self.coords, other.coords))

    def __sub__(self, other):
        other = self._coerce(other)
        return Vector(a - b for a, b in zip(self.coords, other.coords))

    def __neg__(self):
        return Vector(-c for c in self.coords)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(c * other for c in self.coords)
        raise TypeError("Use v.dot(w) or dot(v,w) for dot product, not v*w.")

    def __rmul__(self, other):
        return self.__mul__(other)

    def _coerce(self, other):
        if not isinstance(other, Vector):
            other = Vector(other)
        if len(other) != len(self):
            raise ValueError("Vectors must have same dimension.")
        return other

    # Dot Product
    def dot(self, other):
        other = self._coerce(other)
        return sum(a * b for a, b in zip(self.coords, other.coords))

    # Cross Product
    def cross(self, other):
        other = self._coerce(other)
        if len(self) == 3 and len(other) == 3:
            a1, a2, a3 = self.coords
            b1, b2, b3 = other.coords
            return Vector(a2*b3 - a3*b2,
                          a3*b1 - a1*b3,
                          a1*b2 - a2*b1)
        elif len(self) == 2 and len(other) == 2:
            a1, a2 = self.coords
            b1, b2 = other.coords
            return a1*b2 - a2*b1
        else:
            raise ValueError("Cross product defined for 2D (scalar) or 3D vectors.")

    # Norm + Unit Vector
    def norm(self):
        return sqrt(sum(c*c for c in self.coords))

    def unit(self):
        n = self.norm()
        if n == 0:
            raise ValueError("Zero vector has no unit direction.")
        return (1.0 / n) * self

    def to2d(self):
        if len(self) == 2:
            return self
        elif len(self) >= 2:
            return Vector(self.coords[0], self.coords[1])
        else:
            raise ValueError("Cannot project 1D or empty vector to 2D")



def gradient(f, point, h=1e-5):


    point = tuple(float(x) for x in point)
    n = len(point)
    partials = []
    for i in range(n):
        forward = list(point)
        backward = list(point)
        forward[i] += h
        backward[i] -= h
        df = f(forward) - f(backward)
        partials.append(df / (2*h))
    return Vector(partials)


def vector_derivative(F, t, h=1e-5):


    ft_plus = F(t + h)
    ft_minus = F(t - h)
    if not isinstance(ft_plus, Vector):
        ft_plus = Vector(ft_plus)
    if not isinstance(ft_minus, Vector):
        ft_minus = Vector(ft_minus)
    return (1.0 / (2*h)) * (ft_plus - ft_minus)

def finite_difference(f, x, h=1e-5):

    return (f(x + h) - f(x - h)) / (2*h)


def plot_vectors(vectors, width=600, height=600, padding=60,
                 axis_range=None, show_coords=True, show_grid=True,
                 tick_count=7):

    vs = [v if isinstance(v, Vector) else Vector(v) for v in vectors]
    vs2d = [v.to2d() for v in vs]

    xs = [0.0]; ys = [0.0]
    for v in vs2d:
        xs.append(v.coords[0]); ys.append(v.coords[1])

    if axis_range is None:
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)

        if xmin == xmax: xmin -= 1; xmax += 1
        if ymin == ymax: ymin -= 1; ymax += 1

        dx = xmax - xmin; dy = ymax - ymin
        xmin -= 0.3 * dx; xmax += 0.3 * dx
        ymin -= 0.3 * dy; ymax += 0.3 * dy
    else:
        xmin, xmax, ymin, ymax = axis_range

    def map_point(x, y):
        sx = padding + (x - xmin) / (xmax - xmin) * (width - 2*padding)
        sy = height - (padding + (y - ymin) / (ymax - ymin) * (height - 2*padding))
        return sx, sy

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
               f'style="font-family: sans-serif;">')

    svg.append("""
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="5" refY="5"
          orient="auto" markerUnits="strokeWidth">
    <path d="M0,0 L10,5 L0,10 z" fill="blue"/>
  </marker>
</defs>""")

    svg.append('<rect x="0" y="0" width="100%" height="100%" fill="white"/>')

    ox, oy = map_point(0, 0)

    xticks = [xmin + i*(xmax-xmin)/(tick_count-1) for i in range(tick_count)]
    yticks = [ymin + i*(ymax-ymin)/(tick_count-1) for i in range(tick_count)]

    if show_grid:
        for x in xticks:
            sx, _ = map_point(x, 0)
            svg.append(f'<line x1="{sx}" y1="{padding}" x2="{sx}" y2="{height-padding}" stroke="#eeeeee"/>')
        for y in yticks:
            _, sy = map_point(0, y)
            svg.append(f'<line x1="{padding}" y1="{sy}" x2="{width-padding}" y2="{sy}" stroke="#eeeeee"/>')




    x0,_ = map_point(xmin, 0)
    x1,_ = map_point(xmax, 0)
    _,y0 = map_point(0, ymin)
    _,y1 = map_point(0, ymax)




    svg.append(f'<line x1="{x0}" y1="{oy}" x2="{x1}" y2="{oy}" stroke="black" stroke-width="2"/>')
    svg.append(f'<line x1="{ox}" y1="{y0}" x2="{ox}" y2="{y1}" stroke="black" stroke-width="2"/>')


    for x in xticks:
        sx, sy = map_point(x, 0)
        svg.append(f'<line x1="{sx}" y1="{oy-5}" x2="{sx}" y2="{oy+5}" stroke="black" stroke-width="1.2"/>')
        svg.append(f'<text x="{sx-10}" y="{oy+20}" font-size="14" fill="black" font-family="sans-serif">{x:.1f}</text>')

    for y in yticks:
        sx, sy = map_point(0, y)
        svg.append(f'<line x1="{ox-5}" y1="{sy}" x2="{ox+5}" y2="{sy}" stroke="black" stroke-width="1.2"/>')
        svg.append(f'<text x="{ox+10}" y="{sy+5}" font-size="14" fill="black" font-family="sans-serif">{y:.1f}</text>')







    # Vectors
    for v in vs2d:
        x, y = v.coords
        sx, sy = map_point(x, y)
        svg.append(f'<line x1="{ox}" y1="{oy}" x2="{sx}" y2="{sy}" stroke="blue" stroke-width="2.5" marker-end="url(#arrow)"/>')

        if show_coords:
            svg.append(f'<text x="{sx+8}" y="{sy-8}" font-size="13" font-family="sans-serif">'
                       f'({x:.2f}, {y:.2f})</text>')

    svg.append("</svg>")
    return "\n".join(svg)
