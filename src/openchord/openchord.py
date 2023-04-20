import numpy as np
import drawsvg as dw

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, -y

def get_arc(radius, start_angle, end_angle):
    # calculate coords
    x1, y1 = pol2cart(radius, start_angle)
    x2, y2 = pol2cart(radius, end_angle)
    return x1, y1, x2, y2

def arc(radius, start_angle, end_angle, color="black", opacity=0.9, thickness=0.07):
    # coordinates
    k = 1.0 + thickness
    x1, y1, x2, y2 = get_arc(radius, start_angle, end_angle)
    x3, y3, x4, y4 = k*x2, k*y2, k*x1, k*y1
    # create path 
    p = dw.Path(fill=color, fill_opacity=opacity)
    p.M(x1, y1)
    p.A(radius, radius, rot=0, large_arc=0, sweep=0, ex=x2, ey=y2)
    p.L(x3, y3)
    p.A(k*radius, k*radius, rot=0, large_arc=0, sweep=1, ex=x4, ey=y4).Z()
    return p

def ribbon(radius, source_a1, source_a2, target_a1, target_a2, color="black", opacity=0.6, control_strength=0.6):
    x1, y1, x2, y2 = get_arc(radius, source_a1, source_a2)
    x3, y3, x4, y4 = get_arc(radius, target_a1, target_a2)
    k = 1.0 - control_strength
    xctr1, yctr1, xctr2, yctr2, xctr3, yctr3, xctr4, yctr4 = k*x1, k*y1, k*x2, k*y2, k*x3, k*y3, k*x4, k*y4
    # define path
    p = dw.Path(fill=color, fill_opacity=opacity)
    p.M(x1, y1)
    p.A(radius, radius, rot=0, large_arc=0, sweep=0, ex=x2, ey=y2)
    p.C(xctr2, yctr2, xctr3, yctr3, x3, y3)
    p.A(radius, radius, rot=0, large_arc=0, sweep=0, ex=x4, ey=y4)
    p.C(xctr4, yctr4, xctr1, yctr1, x1, y1)
    p.Z()
    return p

def is_symmetric(A):
        A = np.array(A)
        m, n = A.shape
        if m != n:
            return False
        return np.allclose(A, A.T)

class Chord:
    
    def __init__(self, data, labels=[], fig_size=500, radius=200, gap=0.01):
        self.fig_size = fig_size
        self.data = np.array(data)
        self.labels = labels
        self.radius = radius
        self.shape = self.data.shape[0]
        self.row_sum = np.sum(self.data, axis=0)
        self.total = np.sum(self.data)
        self.gap = gap
        self.font_size = 10
        self.conversion_rate = (2*np.pi-gap*self.shape)/self.total
        self.is_symmetric = is_symmetric(self.data)
        self.ideogram_ends = self.get_ideogram_ends(gap)
        self.ribbon_ends = self.get_ribbon_ends()
        self._color_map = ['#001d5c', '#50216c', '#892070', '#ba2769', '#e1405a', '#fa6644', '#ff9228', '#ffc000']
        self.gradients = self.get_gradients()

    @property
    def color_map(self):
        return self._color_map

    @color_map.setter
    def color_map(self, value):
        self._color_map = value
        self.gradients = self.get_gradients()
        
    def show(self):
        fig = dw.Drawing(self.fig_size, self.fig_size, origin='center')
        # make ideogram
        for i,v in enumerate(self.ideogram_ends):
            fig.append(arc(self.radius, v[0], v[1], color=self.get_color(i)))
        # make ribbon
        for i,v in enumerate(self.ribbon_ends):
            fig.append(ribbon(self.radius*0.99, v[0], v[1], v[2], v[3], color=self.gradients[i]))
        # draw labels
        for i,v in enumerate(self.labels):
            midpoint = np.mean(self.ideogram_ends[i,:])
            x, y = pol2cart(self.radius, midpoint)
            r = np.sqrt(x*x+y*y) * 1.1
            angle = midpoint * 180.0/np.pi
            if midpoint > 0.5*np.pi and midpoint < 1.5*np.pi:
                r *= -1
                angle = -(180.0-angle)
                anchor = "end"
            else:
                anchor = "start"
            fig.append(dw.Text(v, font_size=self.font_size, x=r, y=0, text_anchor=anchor, dominant_baseline='middle', transform=f"rotate(%f)"%(-angle)))
        return fig
    
    def get_ideogram_ends(self, gap):
        arc_lens = self.row_sum * self.conversion_rate
        ideogram_ends = []
        left = 0 
        for arc_len in arc_lens:
            right = left + arc_len
            ideogram_ends.append([left, right])
            left = right + gap
        return np.array(ideogram_ends)
    
    def get_ribbon_ends(self):
        n = self.shape
        arc_lens = self.data * self.conversion_rate
        regions = np.zeros((n, n+1))
        for i in range(n):
            regions[i,0] = self.ideogram_ends[i,0]
            regions[i,1:n+1] = self.ideogram_ends[i,0] + np.cumsum(np.roll(arc_lens[i,::-1], i+1))
        ribbon_ends = []
        for i in range(n):
            ribbon_ends.append([regions[i,0], regions[i,1], regions[i,0], regions[i,1]]) # diagonal terms
        for i in range(n):
            for j in range(i+1, n):
                k = n-j+i
                l = j-i
                ribbon_ends.append([regions[i,k], regions[i,k+1], regions[j,l], regions[j,l+1]])
        return ribbon_ends
    
    def get_gradients(self):
        gradients = []
        idx = 0
        # diagonal terms
        n = self.shape
        for i in range(n):
            gradients.append(self.get_color(i))
            idx += 1
        for i in range(n):
            for j in range(i+1, n):
                a0, a1, a2, a3 = self.ribbon_ends[idx]
                if i == 0 and j == n-1:
                    x0, y0 = pol2cart(self.radius, a1)
                    x1, y1 = pol2cart(self.radius, a2)
                elif np.abs(a3-a0) > np.abs(a2-a1):
                    x0, y0 = pol2cart(self.radius, a0)
                    x1, y1 = pol2cart(self.radius, a3)
                else:
                    x0, y0 = pol2cart(self.radius, a1)
                    x1, y1 = pol2cart(self.radius, a2)
                # create gradient
                g = dw.LinearGradient(x0, y0, x1, y1)
                g.add_stop(0, self.get_color(i))
                g.add_stop(1, self.get_color(j))
                gradients.append(g)
                idx += 1
        return gradients
    
    def save_svg(self, filename):
        fig = self.show()
        fig.save_svg(filename)

    def save_png(self, filename):
        fig = self.show()
        fig.save_png(filename)
    
    def get_color(self, i):
        n = len(self.color_map)
        return self.color_map[i % n]
        