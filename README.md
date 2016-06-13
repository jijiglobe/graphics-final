# graphics-final
graphics final project - Jion Fairchild and Jared Beh

<h3>Added Features:</h3>
<ul>
  <li><h5>Nonlinear Vary</h5></li>
    <ul><li>Vary takes an additional parameter (optional)</li>
    	<li>The addition parameter is N</li>
	<li>If N is provided, animation will be modeled using an order N function</li>
	<li>This means that if n>1, vary will go through higher numbers faster than lower ones</li>
	<li>If 0<n<1, vary will go through lower numbers faster than higher numbers</li>
    </ul>
  <li><h5> Scanline Conversion</h5></li>
    <ul><li>This is enabled automatically and uses both vertical and horizontal scanlines</li>
    </ul>
  <li><h5> Flat Shading </h5></li>
      <ul><li>This uses ambient light, diffuse light, and specular light, to calculate shading of polygons</li>
          <li>This is enabled automatically, and will set the light source to (0,0,0) by default</li>
	  <li>The command <code>shading x y z</code> will set the coordinates of the source to (x,y,z)</li>
	  <li>The shading command should be used before drawing any objects, as it will only be applied after it is called</li>
      </ul>
  <li><h5> Z-buffer </h5></li>
      <ul><li> Objects that are behind other objects will not be drawn </li>
          <li> This feature will be enabled automatically </li>
      </ul>
</ul>