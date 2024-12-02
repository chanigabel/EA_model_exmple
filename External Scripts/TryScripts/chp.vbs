 /*
 * Script Name: ChartAutomation
 * Author:  Sparx Systems
 * Purpose: Enterprise Architect Dynamic Charts Javascript interface
 * Date: 2020
 * Version 1.2
 */

 class ChartCategory {
	static Default(){ return 0;}
	static Line(){ return 1;}
	static Pie(){ return 2;}
	static Pie3D(){ return 3;}
	static Pyramid(){ return 4;}
	static Pyramid3D(){ return 5;}
	static Funnel(){ return 6;}
	static Funnel3D(){ return 7;}
	static Column(){ return 8;}
	static Bar(){ return 9;}
	static Histogram(){ return 10;}
	static Area(){ return 11;}
	static Stock(){ return 12;}
	static Bubble(){ return 13;}
	static LongData(){ return 14;}
	static HistoricalLine(){ return 15;}
	static Polar(){ return 16;}
	static Doughnut(){ return 17;}
	static Doughnut3D(){ return 18;}
	static Torus3D(){ return 19;}
	static Ternary(){ return 20;}
	static Column3D(){ return 21;}
	static Bar3D(){ return 22;}
	static Line3D(){ return 23;}
	static Area3D(){ return 24;}
	static Surface3D(){ return 25;}
	static DoughnutNested(){ return 26;}
	static BoxPlot(){ return 27;}
	static BarSmart(){ return 28;}
	static Bar3DSmart(){ return 29;}
}
	
class ChartType	{
	static DEFAULT(){ return 0;}
	static SIMPLE(){ return 1;}
	static STACKED(){ return 2;}
	static STACKED100(){ return 3;}
	static RANGE(){ return 4;}
}
	
class ChartCurveType {
	static NO_LINE(){ return 0;}
	static LINE(){ return 1;}
	static SPLINE(){ return 2;}			// Kochanek-Bartels spline
	static SPLINE_HERMITE(){ return 3;}	// Hermite spline
	static STEP(){ return 4;}
	static REVERSED_STEP(){ return 5;}
}	
	
class ChartMarkerShape {
	static CIRCLE(){ return 0;}
	static TRIANGLE(){ return 1;}
	static RECTANGLE(){ return 2;}
	static RHOMBUS(){ return 3;}
}

class ChartDrawWallOptions {
	static NONE (){ return  0;}
	static FILL_LEFT_WALL (){ return  0x0001;}
	static OUTLINE_LEFT_WALL (){ return  0x0002;}
	static FILL_RIGHT_WALL (){ return  0x0004;}
	static OUTLINE_RIGHT_WALL (){ return  0x0008;}
	static FILL_FLOOR (){ return  0x0010;}
	static OUTLINE_FLOOR (){ return  0x0020;}
	static DRAW_ALL (){ return  0xFFFF;}
	static DRAW_LEFT_WALL (){ return  ChartDrawWallOptions.FILL_LEFT_WALL() | ChartDrawWallOptions.OUTLINE_LEFT_WALL();}
	static DRAW_RIGHT_WALL (){ return  ChartDrawWallOptions.FILL_RIGHT_WALL() | ChartDrawWallOptions.OUTLINE_RIGHT_WALL();}
	static DRAW_FLOOR (){ return  ChartDrawWallOptions.FILL_FLOOR() | ChartDrawWallOptions.OUTLINE_FLOOR();}
	static DRAW_ALL_WALLS (){ return  ChartDrawWallOptions.DRAW_LEFT_WALL() | ChartDrawWallOptions.DRAW_RIGHT_WALL();}
	static OUTLINE_ALL_WALLS (){ return  ChartDrawWallOptions.OUTLINE_LEFT_WALL() | ChartDrawWallOptions.OUTLINE_RIGHT_WALL();}
	static OUTLINE_ALL (){ return  ChartDrawWallOptions.OUTLINE_ALL_WALLS() | ChartDrawWallOptions.OUTLINE_FLOOR();}
	static FILL_ALL_WALLS (){ return  ChartDrawWallOptions.FILL_LEFT_WALL() | ChartDrawWallOptions.FILL_RIGHT_WALL();}
	static FILL_ALL (){ return  ChartDrawWallOptions.FILL_ALL_WALLS() | ChartDrawWallOptions.FILL_FLOOR();}
	static DEFAULT (){ return  ChartDrawWallOptions.OUTLINE_ALL();}
}

class ChartAxisType {
	static Y_PRIMARY_AXIS(){ return 0;}
	static Y_SECONDARY_AXIS(){ return 1;}
	static X_PRIMARY_AXIS(){ return 2;}
	static X_SECONDARY_AXIS(){ return 3;}
	static Z_PRIMARY_AXIS(){ return 4;}
	static Z_SECONDARY_AXIS(){ return 5;}
	static Y_POLAR_AXIS(){ return 6;}
	static X_POLAR_AXIS(){ return 7;}
	static A_TERNARY_AXIS(){ return 8;}
	static B_TERNARY_AXIS(){ return 9;}
	static C_TERNARY_AXIS(){ return 10;}
}

class ChartLabelContent
{
	static DEFAULT() { return 0x0; }
	static SERIES_NAME(){ return 0x01; }
	static CATEGORY_NAME(){ return 0x02; }
	static VALUE(){ return 0x04; }
	static PERCENTAGE(){ return 0x08; }
	static X_VALUE(){ return 0x10; }
	static BUBBLE_SIZE(){ return 0x20; }
	static Y1_VALUE(){ return 0x40; }
	static Y2_VALUE(){ return 0x80; }
	static A_TERNARY_PERCENTAGE(){ return ChartLabelContent.PERCENTAGE(); }
	static B_TERNARY_PERCENTAGE(){ return 0x100; }
	static C_TERNARY_PERCENTAGE(){ return 0x200; }
	static DP_INDEX(){ return 0x400;}
	static A_TERNARY_VALUE(){ return ChartLabelContent.VALUE(); }
	static B_TERNARY_VALUE(){ return ChartLabelContent.Y1_VALUE(); }
	static C_TERNARY_VALUE(){ return ChartLabelContent.Y2_VALUE(); }
	static BUBBLE_VALUES(){ return ChartLabelContent.VALUE() | ChartLabelContent.X_VALUE() | ChartLabelContent.BUBBLE_SIZE();}
	static ALL_BUBBLE_VALUES(){ return ChartLabelContent.SERIES_NAME() | ChartLabelContent.VALUE() | ChartLabelContent.X_VALUE() | ChartLabelContent.BUBBLE_SIZE(); }
	static VALUE_PERCENTAGE(){ return ChartLabelContent.VALUE() | ChartLabelContent.PERCENTAGE(); }
	static SERIES_VALUES(){ return ChartLabelContent.SERIES_NAME() | ChartLabelContent.VALUE() | ChartLabelContent.X_VALUE(); }
	static SERIES_CATEGORY_VALUE(){ return ChartLabelContent.SERIES_NAME() | ChartLabelContent.CATEGORY_NAME() | ChartLabelContent.VALUE(); }
	static PIE_NAME_PERCENTAGE(){ return ChartLabelContent.CATEGORY_NAME() | ChartLabelContent.PERCENTAGE(); }
	static ALL_TERNARY_VALUES(){ return ChartLabelContent.A_TERNARY_VALUE() | ChartLabelContent.B_TERNARY_VALUE() | ChartLabelContent.C_TERNARY_VALUE();}
	static ALL_TERNARY_PERCENTAGE(){ return ChartLabelContent.A_TERNARY_PERCENTAGE() | ChartLabelContent.B_TERNARY_PERCENTAGE() | ChartLabelContent.C_TERNARY_PERCENTAGE(); }
}
	
class ChartDashStyle
{
	static SOLID() { return 0; ;}
	static DASH() { return 1; ;}
	static DOT() { return 2; ;}
	static DASH_DOT() { return 3; ;}
	static DASH_DOT_DOT() { return 4; ;}
	static CUSTOM() { return 5; ;}
}

class ChartSurfaceType	{
	static STANDARD(){ return 0;}
	static LEVELS(){ return 1;}
}

function ChartSurfaceTypeFromString( key)
{
	var rval = ChartSurfaceType.STANDARD();
	switch(key)
	{
		case "Levels":
		{
			rval = ChartSurfaceType.LEVELS();
		}
	}
	return rval;
}

class ChartColorMode
{
	static SINGLE(){ return 0;}
	static MULTIPLE(){ return 1;}
	static PALETTE(){ return 2;}
	static CUSTOM(){ return 3;}
	static SERIES(){ return 4;}
}

class ChartFrameStyle {
	static NONE(){ return 0;}
	static MESH(){ return 1;}
	static CONTOUR(){ return 2;}
	static CONTOUR_MESH(){ return 3;}
}

class ChartLevelRangeMode {
	static MINMAX_SERIES(){ return 0;}
	static MINMAX_Y_AXIS(){ return 1;}
	static CUSTOM(){ return 2;}
}

class ChartColor
{
	static Default (){ return -1;}
	static AliceBlue (){ return  0xF0F8FF;}
	static AntiqueWhite (){ return  0xFAEBD7;}
	static Aqua (){ return  0x00FEFE;}
	static Aquamarine (){ return  0x7FFFD4;}
	static Azure (){ return  0xF0FFFF;}
	static Beige (){ return  0xF5F5DC;}
	static Bisque (){ return  0xFFE4C4;}
	static Black (){ return  0x000000;}
	static BlanchedAlmond (){ return  0xFFEBCD;}
	static Blue (){ return  0x0000FF;}
	static BlueViolet (){ return  0x8A2BE2;}
	static Brown (){ return  0xA52A2A;}
	static BurlyWood (){ return  0xDEB887;}
	static CadetBlue (){ return  0x5F9EA0;}
	static Chartreuse (){ return  0x7FFF00;}
	static Chocolate (){ return  0xD2691E;}
	static Coral (){ return  0xFF7F50;}
	static CornflowerBlue (){ return  0x6495ED;}
	static Cornsilk (){ return  0xFFF8DC;}
	static Crimson (){ return  0xDC143C;}
	static Cyan (){ return  0x00FFFF;}
	static DarkBlue (){ return  0x00008B;}
	static DarkCyan (){ return  0x008B8B;}
	static DarkGoldenrod (){ return  0xB8860B;}
	static DarkGray (){ return  0xA9A9A9;}
	static DarkGreen (){ return  0x006400;}
	static DarkKhaki (){ return  0xBDB76B;}
	static DarkMagenta (){ return  0x8B008B;}
	static DarkOliveGreen (){ return  0x556B2F;}
	static DarkOrange (){ return  0xFF8C00;}
	static DarkOrchid (){ return  0x9932CC;}
	static DarkRed (){ return  0x8B0000;}
	static DarkSalmon (){ return  0xE9967A;}
	static DarkSeaGreen (){ return  0x8FBC8F;}
	static DarkSlateBlue (){ return  0x483D8B;}
	static DarkSlateGray (){ return  0x4F4F4F;}
	static DarkTurquoise (){ return  0x00CED1;}
	static DarkViolet (){ return  0x9400D3;}
	static DeepPink (){ return  0xFF1493;}
	static DeepSkyBlue (){ return  0x00BFFF;}
	static DimGray (){ return  0x696969;}
	static DodgerBlue (){ return  0x1E90FF;}
	static Firebrick (){ return  0xB22222;}
	static FloralWhite (){ return  0xFFFAF0;}
	static ForestGreen (){ return  0x228B22;}
	static Fuchsia (){ return  0xFE00FE;}
	static Gainsboro (){ return  0xDCDCDC;}
	static GhostWhite (){ return  0xF8F8FF;}
	static Gold (){ return  0xFFD700;}
	static Goldenrod (){ return  0xDAA520;}
	static Gray (){ return  0x808080;}
	static Green (){ return  0x008000;}
	static GreenYellow (){ return  0xADFF2F;}
	static Honeydew (){ return  0xF0FFF0;}
	static HotPink (){ return  0xFF69B4;}
	static IndianRed (){ return  0xCD5C5C;}
	static Indigo (){ return  0x4B0082;}
	static Ivory (){ return  0xFFFFF0;}
	static Khaki (){ return  0xF0E68C;}
	static Lavender (){ return  0xE6E6FA;}
	static LavenderBlush (){ return  0xFFF0F5;}
	static LawnGreen (){ return  0x7CFC00;}
	static LemonChiffon (){ return  0xFFFACD;}
	static LightBlue (){ return  0xADD8E6;}
	static LightCoral (){ return  0xF08080;}
	static LightCyan (){ return  0xE0FFFF;}
	static LightGoldenrodYellow (){ return  0xFAFAD2;}
	static LightGreen (){ return  0x90EE90;}
	static LightGray (){ return  0xD3D3D3;}
	static LightPink (){ return  0xFFB6C1;}
	static LightSalmon (){ return  0xFFA07A;}
	static LightSeaGreen (){ return  0x20B2AA;}
	static LightSkyBlue (){ return  0x87CEFA;}
	static LightSlateGray (){ return  0x778899;}
	static LightSteelBlue (){ return  0xB0C4DE;}
	static LightYellow (){ return  0xFFFFE0;}
	static Lime (){ return  0x00FF00;}
	static LimeGreen (){ return  0x32CD32;}
	static Linen (){ return  0xFAF0E6;}
	static Magenta (){ return  0xFF00FF;}
	static Maroon (){ return  0x800000;}
	static MediumAquamarine (){ return  0x66CDAA;}
	static MediumBlue (){ return  0x0000CD;}
	static MediumOrchid (){ return  0xBA55D3;}
	static MediumPurple (){ return  0x9370DB;}
	static MediumSeaGreen (){ return  0x3CB371;}
	static MediumSlateBlue (){ return  0x7B68EE;}
	static MediumSpringGreen (){ return  0x00FA9A;}
	static MediumTurquoise (){ return  0x48D1CC;}
	static MediumVioletRed (){ return  0xC71585;}
	static MidnightBlue (){ return  0x191970;}
	static MintCream (){ return  0xF5FFFA;}
	static MistyRose (){ return  0xFFE4E1;}
	static Moccasin (){ return  0xFFE4B5;}
	static NavajoWhite (){ return  0xFFDEAD;}
	static Navy (){ return  0x000080;}
	static OldLace (){ return  0xFDF5E6;}
	static Olive (){ return  0x808000;}
	static OliveDrab (){ return  0x6B8E23;}
	static Orange (){ return  0xFFA500;}
	static OrangeRed (){ return  0xFF4500;}
	static Orchid (){ return  0xDA70D6;}
	static PaleGoldenrod (){ return  0xEEE8AA;}
	static PaleGreen (){ return  0x98FB98;}
	static PaleTurquoise (){ return  0xAFEEEE;}
	static PaleVioletRed (){ return  0xDB7093;}
	static PapayaWhip (){ return  0xFFEFD5;}
	static PeachPuff (){ return  0xFFDAB9;}
	static Peru (){ return  0xCD853F;}
	static Pink (){ return  0xFFC0CB;}
	static Plum (){ return  0xDDA0DD;}
	static PowderBlue (){ return  0xB0E0E6;}
	static Purple (){ return  0x800080;}
	static Red (){ return  0xFF0000;}
	static RosyBrown (){ return  0xBC8F8F;}
	static RoyalBlue (){ return  0x4169E1;}
	static SaddleBrown (){ return  0x8B4513;}
	static Salmon (){ return  0xFA8072;}
	static SandyBrown (){ return  0xF4A460;}
	static SeaGreen (){ return  0x2E8B57;}
	static SeaShell (){ return  0xFFF5EE;}
	static Sienna (){ return  0xA0522D;}
	static Silver (){ return  0xC0C0C0;}
	static SkyBlue (){ return  0x87CEEB;}
	static SlateBlue (){ return  0x6A5ACD;}
	static SlateGray (){ return  0x708090;}
	static Snow (){ return  0xFFFAFA;}
	static SpringGreen (){ return  0x00FF7F;}
	static SteelBlue (){ return  0x4682B4;}
	static Tan (){ return  0xD2B48C;}
	static Teal (){ return  0x008080;}
	static Thistle (){ return  0xD8BFD8;}
	static Tomato (){ return  0xFF6347;}
	static Turquoise (){ return  0x40E0D0;}
	static Violet (){ return  0xEE82EE;}
	static Wheat (){ return  0xF5DEB3;}
	static White (){ return  0xFFFFFF;}
	static WhiteSmoke (){ return  0xF5F5F5;}
	static Yellow (){ return  0xFFFF00;}
	static YellowGreen (){ return  0x9ACD32;}
}

class RenderingType
{
	static SOFTWARE() { return 0;}
	static OPENGL() { return 1;}
}

function RenderingEngineFromString( key)
{
	var rval = RenderingType.SOFTWARE();
	switch(key)
	{
		case "OpenGL":
			rval = RenderingType.OPENGL();
		    break;
	}
	return rval;
}

class ChartAnimationType
{
	static Legacy () { return 0; }	// Timer-based linear animation
	static AccelerateDecelerate() { return 1; }
	static Cubic() { return 2; }
	static Linear() { return 3; }
	static SmoothStop() { return 4; }
	static ParabolicFromAcceleration() { return 5; }
}
	
class ChartAnimationStyle
{
	static Default() { return 0; }
	static None() { return 1; }
	static Grow() { return 2; }
	static Fade() { return 3; }
	static Slide() { return 4; }
	static SlideReversed() { return 5; }
}
	
class ChartFeature
{
	static Unknown(){ return -1; }
	static ClusteredBar2D() { return 0; }
	static ClusteredColumn2D() { return 1; }
	static StackedBarSideBySide2D() { return 2; }
	static StackedColumnSideBySide2D() { return 3; }
	static StackedBar2D() { return 4; }
	static StackedBar1002D() { return 5; }
	static StackedColumn1002D() { return 6; }
	static StackedColumn2D() { return 7;}
	static ClusteredBar3D() { return 8; }
	static ClusteredColumn3D() { return 9; }
	static StackedBarSideBySide3D() { return 10; }
	static StackedColumnSideBySide3D() { return 11; }
	static StackedBar3D() { return 12; }
	static StackedBar1003D() { return 13; }
	static StackedColumn1003D() { return 14; }
	static StackedColumn3D() { return 15;}
	static StackedColumnManhattan3D() { return 16;}
}

class ChartGradient
{
	static NONE() { return 0; }
	static HORIZONTAL() { return 1; }
	static VERTICAL() { return 2; }
	static DIAGONAL_LEFT() { return 3; }
	static DIAGONAL_RIGHT() { return 4; }
	static CENTER_HORIZONTAL() { return 5; }
	static CENTER_VERTICAL() { return 6; }
	static RADIAL_TOP() { return 7; }
	static RADIAL_CENTER() { return 8; }
	static RADIAL_BOTTOM() { return 9; }
	static RADIAL_LEFT() { return 10; }
	static RADIAL_RIGHT() { return 11; }
	static RADIAL_TOP_LEFT() { return 12; }
	static RADIAL_TOP_RIGHT() { return 13; }
	static RADIAL_BOTTOM_LEFT() { return 14; }
	static RADIAL_BOTTOM_RIGHT() { return 15; }
	static BEVEL() { return 16; }
	static PIPE_VERTICAL() { return 17; }
	static PIPE_HORIZONTAL() { return 18; }
}

class BarShape
{
	static Box() { return 0;}
	static Pyramid() { return 1;}
	static PyramidPartial() { return 2;}
}

class ChartDataIndex
{
	static Default() { return -1; }
	static Y() { return 0; }
	static X() { return 1; }
	static Z() { return 2; }
	static Y1() { return 3; }
	static Y2() { return 4; }
	static Y3() { return 5; }
	static Percentage() { return 6; }
	static Custom() { return 7; }
	static GroupValue() { return 8; }
	static GroupPercentage() { return 9; }
}

class ChartStockSeriesKind
{
	static Undefined() { return 0;}
	static Open() { return 1;}
	static High() { return 2;}
	static Low() { return 3;}
	static Close() { return 5;}
};

class ChartStockSeriesType
{
	static Bar() { return 0;}
	static Candle() { return 1;}
	static LineOpen() { return 2;}
	static LineHigh() { return 3;}
	static LineLow() { return 4;}
	static LineClose() { return 5;}
	static LineCustom() { return 6;}
}

class ChartAxisIndex
{
	static UNKNOWN() { return -1; }
	static X() { return 0; }
	static Y() { return 1; }
	static Z() { return 2; }
}

class ChartAxisTickMarkType
{
	static NO_TICKS(){ return 0;}
	static INSIDE(){ return 1;}
	static OUTSIDE(){ return 2;}
	static CROSS(){ return 3;}
};

class ChartAxisLabelType
{
	static NO_LABELS(){ return 0;}
	static NEXT_TO_AXIS(){ return 1;}
	static HIGH(){ return 2;}
	static LOW(){ return 3;}
};

class ChartAxisCrossType
{
	static AUTO(){ return 0;}
	static MAXIMUM_AXIS_VALUE(){ return 1;}
	static MINIMUM_AXIS_VALUE(){ return 2;}
	static AXIS_VALUE(){ return 3;}
	static IGNORE(){ return 4;}
	static FIXED_DEFAULT_POS(){ return 5;}
};

class  ChartAxisDefaultPosition
{
	static LEFT(){ return 0;}
	static BOTTOM(){ return 1;}
	static RIGHT(){ return 2;}
	static TOP(){ return 3;}
	static DEPTH_BOTTOM(){ return 4;}
	static DEPTH_TOP(){ return 5;}
};

class ChartAxisRoundType
{
	static EXACT(){ return 0;}
	static FLOOR(){ return 1;}
	static CEIL(){ return 2;}
	static ROUND(){ return 3}
};

class ChartDatasourceType
{
	static Unknown() { return 0; }
	static JSON() { return 1; }
	static XML() { return 2;}
	static Javascript() { return 3; }
};
	
class ChartDatapointType
{
	static Normal() { return 0; }
	static Stock() { return 1; }
	static Column() { return 2;}
};

class ChartLabelPosition
{	
	static Default() { return 0;}
	static Center() { return 1;}
	static InsideEnd() { return 2;}
	static InsideBase() { return 3;}
	static OutsideEnd() { return 4;}
}

var relatedAxis=new Object;

function toDouble( rVal )
{
	if(typeof rVal == "string")
	{
		var date = new Date(rVal);
		return date.getTime();
	}
	return rVal;
}

function ChartAxisCrossTypeFromString( key )
{
	var rVal = ChartAxisCrossType.AUTO(); 
	switch(key )
	{
		case "MinimumValue":
			 rVal = ChartAxisCrossType.MINIMUM_AXIS_VALUE();
			 break;
		case "MaximumValue":
			 rVal = ChartAxisCrossType.MAXIMUM_AXIS_VALUE();
			 break;
		case "AxisValue":
			 rVal = ChartAxisCrossType.AXIS_VALUE();
			 break;
		case "Ignore":
			 rVal = ChartAxisCrossType.IGNORE();
			 break;
		case "Fixed":
			 rVal = ChartAxisCrossType.FIXED_DEFAULT_POS();
			 break;
	}
	return rVal;
}

function ChartAxisTickMarkFromString( key )
{
	var rVal = ChartAxisTickMarkType.NO_TICKS(); 
	switch(key )
	{
		case "Inside":
			 rVal = ChartAxisTickMarkType.INSIDE();
			 break;
		case "Outside":
			 rVal = ChartAxisTickMarkType.OUTSIDE();
			 break;
		case "Cross":
			 rVal = ChartAxisTickMarkType.CROSS();
			 break;
	}
	return rVal;
}

function ChartAxisIndexFromString( key )
{
	var rVal = ChartAxisIndex.UNKNOWN();
	switch(key)
	{
		case "X":
			rVal = ChartAxisIndex.X();
			break;
		case "Y":
			rVal = ChartAxisIndex.Y();
			break;
		case "Z":
			rVal = ChartAxisIndex.Z();
			break;
	} 
	return rVal;
}

function ChartStockSeriesTypeFromString( key )
{
	var rVal = ChartStockSeriesType.LineOpen(); 
	switch(key )
	{
		case "Bar":
			 rVal = ChartStockSeriesType.Bar();
			 break;
		case "Candle":
			 rVal = ChartStockSeriesType.Candle();
			 break;
		case "LineOpen":
			 rVal = ChartStockSeriesType.LineOpen();
			 break;
		case "LineHigh":
			 rVal = ChartStockSeriesType.LineHigh();
			 break;
		case "LineLow":
			 rVal = ChartStockSeriesType.LineLow();
			 break;
		case "LineClose":
			 rVal = ChartStockSeriesType.LineClose();
			 break;
		case "LineCustom":
			 rVal = ChartStockSeriesType.LineCustom();
			 break;
	}
	return rVal;
}

function ChartCategoryFromString( key )
{
	var rVal = ChartCategory.Default(); 
	switch(key )
	{
		case "Area":
			 rVal = ChartCategory.Area();
			 break;
		case "Area3D":
			 rVal = ChartCategory.Area3D();
			 break;
		case "Bar":
			 rVal = ChartCategory.Bar();
			 break;
		case "Bar3D":
			 rVal = ChartCategory.Bar3D();
			 break;
		case "BarSmart":
			 rVal = ChartCategory.BarSmart();
			 break;
		case "Column":
			 rVal = ChartCategory.Column();
			 break;
		case "Column3D":
			 rVal = ChartCategory.Column3D();
			 break;
		case "Line":
			 rVal = ChartCategory.Line();
			 break;
		case "Line3D":
			 rVal = ChartCategory.Line3D();
			 break;
		case "Polar":
			 rVal = ChartCategory.Polar();
			 break;
		case "Stock":
			 rVal = ChartCategory.Stock();
			 break;
		case "Surface3D":
			 rVal = ChartCategory.Surface3D();
			 break;
		case "Pie":
			 rVal = ChartCategory.Pie();
			 break;
		case "Pie3D":
			 rVal = ChartCategory.Pie3D();
			 break;
		case "Histogram":
			 rVal = ChartCategory.Histogram();
			 break;
		case "BoxPlot":
			 rVal = ChartCategory.BoxPlot();
			 break;
	}
	return rVal;
}
function ChartTypeFromString( key )
{
	var rVal = ChartType.DEFAULT(); 
	switch(key )
	{
		case "Simple":
			 rVal = ChartType.SIMPLE();
			 break;
		case "Range":
			 rVal = ChartType.RANGE();
			 break;
		case "Stacked":
			 rVal = ChartType.STACKED();
			 break;
		case "Stacked100":
			 rVal = ChartType.STACKED100();
			 break;
	}
	return rVal;
}

function ChartFrameStyleFromString( key )
{
	var rVal = ChartFrameStyle.MESH(); 
	switch(key )
	{
		case "None":
			 rVal = ChartFrameStyle.NONE();
			 break;
		case "Mesh":
			 rVal = ChartFrameStyle.MESH();
			 break;
		case "Contour":
			 rVal = ChartFrameStyle.CONTOUR();
			 break;
		case "ContourMesh":
			 rVal = ChartFrameStyle.CONTOUR_MESH();
			 break;
	}
	return rVal;
}

function ChartColorModeFromString( key )
{
	var rVal = ChartColorMode.MULTIPLE(); 
	switch(key )
	{
		case "Single":
			 rVal = ChartColorMode.SINGLE();
			 break;
		case "Multiple":
			 rVal = ChartColorMode.MULTIPLE();
			 break;
		case "Palette":
			 rVal = ChartColorMode.PALETTE();
			 break;
		case "Series":
			 rVal = ChartColorMode.SERIES();
			 break;
		case "Custom":
			 rVal = ChartColorMode.CUSTOM();
			 break;
	}
	return rVal;
}

function ChartCurveTypeFromString( key )
{
	var rVal = ChartCurveType.LINE(); 
	switch(key )
	{
		case "Line":
			 rVal = ChartCurveType.LINE();
			 break;
		case "NoLine":
			 rVal = ChartCurveType.NO_LINE();
			 break;
		case "Step":
			 rVal = ChartCurveType.STEP();
			 break;
		case "ReversedStep":
			 rVal = ChartCurveType.REVERSED_STEP();
			 break;
		case "Spline":
			 rVal = ChartCurveType.SPLINE();
			 break;
		case "SplineHermite":
			 rVal = ChartCurveType.SPLINE_HERMITE();
			 break;
	}
	return rVal;
}

function ChartAxisTypeFromString( key)
{
	var rVal = 0;
	switch(key)
	{
		case "PrimaryY":
			rVal = ChartAxisType.Y_PRIMARY_AXIS();
			break;
		case "SecondaryY":
			rVal = ChartAxisType.Y_SECONDARY_AXIS();
			break;
		case "PrimaryX":
			rVal = ChartAxisType.X_PRIMARY_AXIS();
			break;
		case "SecondaryX":
			rVal = ChartAxisType.X_SECONDARY_AXIS();
			break;
		case "PrimaryZ":
			rVal = ChartAxisType.Z_PRIMARY_AXIS();
			break;
		case "SecondaryZ":
			rVal = ChartAxisType.Z_SECONDARY_AXIS();
			break;
		case "PolarY":
			rVal = ChartAxisType.Y_POLAR_AXIS();
			break;
		case "PolarX":
			rVal = ChartAxisType.X_POLAR_AXIS();
			break;
		case "TernaryA":
			rVal = ChartAxisType.A_TERNARY_AXIS();
			break;
		case "TernaryB":
			rVal = ChartAxisType.B_TERNARY_AXIS();
			break;
		case "TernaryC":
			rVal = ChartAxisType.C_TERNARY_AXIS();
			break;
	}
	return rVal;
}

function ChartDashStyleFromString( key )
{
	var rVal = ChartDashStyle.CUSTOM();
	switch(key)
	{
		case "Solid":
			rVal = ChartDashStyle.SOLID();
			break;
		case "Dash":
			rVal = ChartDashStyle.DASH();
			break;
		case "Dot":
			rVal = ChartDashStyle.DOT();
			break;
		case "DashDot":
			rVal = ChartDashStyle.DASH_DOT();
			break;
		case "DashDotDot":
			rVal = ChartDashStyle.DASH_DOT_DOT();
			break;
	}
	return rVal;
}

function ChartShapeFromString( key )
{
	var rVal = ChartMarkerShape.RECTANGLE(); 
	switch(key )
	{
		case "Circle":
			 rVal = ChartMarkerShape.CIRCLE();
			 break;
		case "Rectangle":
			 rVal = ChartMarkerShape.RECTANGLE();
			 break;
		case "Triangle":
			 rVal = ChartMarkerShape.TRIANGLE();
			 break;
		case "Rhombus":
			 rVal = ChartMarkerShape.RHOMBUS();
			 break;
	}
	return rVal;
}

function ChartDatasourceTypeFromString( key)
{
	var rVal = ChartDatasourceType.Unknown(); 
	switch(key )
	{
		case "Javascript":
			 rVal = ChartMarkerShape.Javascript();
			 break;
		case "JSON":
			 rVal = ChartMarkerShape.JSON();
			 break;
		case "XML":
			 rVal = ChartMarkerShape.XML();
			 break;
	}
	return rVal;
}

function ChartLevelRangeModeFromString(key)
{
	var rVal = ChartLevelRangeMode.CUSTOM(); 
	switch(key )
	{
		case "MinMaxSeries":
			 rVal = ChartLevelRangeMode.MINMAX_SERIES();
			 break;
		case "MinMaxAxisY":
			 rVal = ChartLevelRangeMode.MINMAX_Y_AXIS();
			 break;
	}
	return rVal;
}

function ChartGradientTypeFromString( key )
{
	var rVal = ChartGradient.NONE();
	switch(key)
	{
		case "Horizontal":
			 rVal = ChartGradient.HORIZONTAL();
		     break;
		case "Vertical":
			 rVal = ChartGradient.VERTICAL();
		     break;
		case "DiagonalLeft":
			 rVal = ChartGradient.DIAGONAL_LEFT();
		     break;
		case "DiagonalRight":
			 rVal = ChartGradient.DIAGONAL_RIGHT();
		     break;
		case "CenterHorizontal":
			 rVal = ChartGradient.CENTER_HORIZONTAL();
		     break;
		case "CenterVertical":
			 rVal = ChartGradient.CENTER_VERTICAL();
		     break;
		case "RadialTop":
			 rVal = ChartGradient.RADIAL_TOP();
		     break;
		case "RadialCenter":
			 rVal = ChartGradient.RADIAL_CENTER();
		     break;
		case "RadialBottom":
			 rVal = ChartGradient.RADIAL_BOTTOM();
		     break;
		case "RadialLeft":
			 rVal = ChartGradient.RADIAL_LEFT();
		     break;
		case "RadialRight":
			 rVal = ChartGradient.RADIAL_RIGHT();
		     break;
		case "RadialTopLeft":
			 rVal = ChartGradient.RADIAL_TOP_LEFT();
		     break;
		case "RadialTopRight":
			 rVal = ChartGradient.RADIAL_TOP_RIGHT();
		     break;
		case "RadialBottomLeft":
			 rVal = ChartGradient.RADIAL_BOTTOM_LEFT();
		     break;
		case "RadialBottomRight":
			 rVal = ChartGradient.RADIAL_BOTTOM_RIGHT();
		     break;
		case "Bevel":
			 rVal = ChartGradient.BEVEL();
		     break;
		case "PipeVertical":
			 rVal = ChartGradient.PIPE_VERTICAL();
		     break;
		case "PipeHorizontal":
			 rVal = ChartGradient.PIPE_HORIZONTAL();
		     break;
	}
	return rVal;
}

function ChartLabelContentFromString( key )
{
	var rVal = ChartLabelContent.DEFAULT();
	switch(key)
	{
		case "SeriesName":
			 rVal = ChartLabelContent.SERIES_NAME();
		     break;
		case "CategoryName":
			 rVal = ChartLabelContent.CATEGORY_NAME();
		     break;
		case "Value":
			 rVal = ChartLabelContent.VALUE();
		     break;
		case "Percentage":
			 rVal = ChartLabelContent.PERCENTAGE();
		     break;
		case "XValue":
			 rVal = ChartLabelContent.X_VALUE();
		     break;
		case "BubbleSize":
			 rVal = ChartLabelContent.BUBBLE_SIZE();
		     break;
		case "Y1Value":
			 rVal = ChartLabelContent.Y1_VALUE();
		     break;
		case "Y2Value":
			 rVal = ChartLabelContent.Y2_VALUE();
		     break;
		case "TernaryPercentageA":
			 rVal = ChartLabelContent.A_TERNARY_PERCENTAGE();
		     break;
		case "TernaryPercentageB":
			 rVal = ChartLabelContent.B_TERNARY_PERCENTAGE();
		     break;
		case "TernaryPercentageC":
			 rVal = ChartLabelContent.C_TERNARY_PERCENTAGE();
		     break;
		case "DPIndex":
			 rVal = ChartLabelContent.DP_INDEX();
		     break;
		case "TernaryValueA":
			 rVal = ChartLabelContent.A_TERNARY_VALUE();
		     break;
		case "TernaryValueB":
			 rVal = ChartLabelContent.B_TERNARY_VALUE();
		     break;
		case "TernaryValueC":
			 rVal = ChartLabelContent.C_TERNARY_VALUE();
		     break;
		case "BubbleValues":
			 rVal = ChartLabelContent.BUBBLE_VALUES();
		     break;
		case "AllBubbleValues":
			 rVal = ChartLabelContent.ALL_BUBBLE_VALUES();
		     break;
		case "ValuePercentage":
			 rVal = ChartLabelContent.VALUE_PERCENTAGE();
		     break;
		case "SeriesValues":
			 rVal = ChartLabelContent.SERIES_VALUES();
		     break;
		case "SeriesCategoryValue":
			 rVal = ChartLabelContent.SERIES_CATEGORY_VALUE();
		     break;
		case "PieNamePercentage":
			 rVal = ChartLabelContent.PIE_NAME_PERCENTAGE();
		     break;
		case "AllTernaryValues":
			 rVal = ChartLabelContent.ALL_TERNARY_VALUES();
		     break;
		case "AllTernaryPercentage":
			 rVal = ChartLabelContent.ALL_TERNARY_PERCENTAGE();
		     break;
	}
	return rVal;
}

function ChartLabelPositionFromString( key )
{
	var rVal = ChartLabelPosition.Default();
	switch(key)
	{
		case "Center":
			 rVal = ChartLabelPosition.Center();
		     break;
		case "InsideEnd":
			 rVal = ChartLabelPosition.InsideEnd();
		     break;
		case "OutsideEnd":
			 rVal = ChartLabelPosition.OutsideEnd();
		     break;
		case "InsideBase":
			 rVal = ChartLabelPosition.InsideBase();
		     break;
	}
	return rVal;
}

function LegendDescriptor()
{
	this.nValue = 0;
	this.bIndexed=false;
	this.bLegend = false;

	this.Reset = function()	{
		this.nValue = 0;
		this.bLegend = false;
		this.bIndexed=false;
	}
	this.ParseLegend = function( pProperty )
	{
		this.bLegend=true;
		this.bIndexed=false;
		if(Array.isArray(pProperty))		{
			for(var e=0; e < pProperty.length; e++) 	{
				if(pProperty[e]=="DPIndex")
					this.bIndexed=true;
				this.nValue |= ChartLabelContentFromString( pProperty[e] );
			}
		}
		else {
			this.bIndexed = (pProperty==="DPIndex");
			this.nValue |= ChartLabelContentFromString( pProperty );
		}
		return true;
	}
}

var chartLegendDescriptor = new LegendDescriptor();

// can test existence of element index for an array
function propExists( obj, prop)
{
	if(typeof obj === "undefined")
		return false;
	return obj.hasOwnProperty(prop);
}

function SetChartAttributes( chart, jsonObj)
{
	chartLegendDescriptor.Reset();
	
	if(!propExists( jsonObj, "Category"))
	{
		return false;
	}
	if(!propExists( jsonObj, "Type"))
	{
		return false;
	}
	var chartCategory = ChartCategoryFromString(jsonObj.Category);
	var chartType = ChartTypeFromString(jsonObj.Type);
	chart.SetChartType( chartCategory, chartType, false, true);
	
	if(propExists( jsonObj, "Title"))
	{
		chart.Title = jsonObj.Title;
	}
	if(propExists( jsonObj, "CurveType"))
	{
		chart.SetCurveType(ChartCurveTypeFromString(jsonObj.CurveType));
	}	
	if(propExists(jsonObj,"DataMarkers"))
	{
		var markers =jsonObj.DataMarkers;
		chart.ShowDataMarkers( markers.Visible, markers.Size, ChartShapeFromString(markers.Shape));
	}
	if(propExists( jsonObj, "Opacity"))
	{
		chart.SetThemeOpacity(jsonObj.Opacity);
	}
	if(propExists( jsonObj, "Diagram"))
	{
		var dgm = jsonObj.Diagram;
		if(propExists( dgm, "Engine"))
		{
			var engine = RenderingEngineFromString(dgm.Engine);
			var diagram = chart.GetDiagram3D();
			if(diagram)
			{
				diagram.SetRenderingType( engine );
			}
		}
	}
	if(propExists( jsonObj,"DataLabels"))
	{
		var dataLabels = jsonObj.DataLabels;
		var bBorder = false;
		var bDrop=false;
		var dAngle = 45.0;
		var bVisible = false;

		if(propExists( dataLabels, "Visible"))
			bVisible = dataLabels.Visible;
		if(propExists( dataLabels, "Border"))
			bBorder = dataLabels.Border;
		if(propExists( dataLabels, "DropLineToMarker"))
			bDrop = dataLabels.DropLineToMarker;
		if(propExists( dataLabels, "Angle"))
			dAngle = dataLabels.Angle;
		
		chart.ShowDataLabels( bVisible, bBorder, bDrop, dAngle);

		if(propExists( dataLabels, "Legend"))
			chartLegendDescriptor.ParseLegend(dataLabels.Legend);

	}
	
	return true;
}

function DefineAxis( axis, jsonAxis)
{
	if(propExists(jsonAxis,"Label"))
		axis.SetAxisName(jsonAxis.Label,true);

	if(propExists(jsonAxis,"DataFormat"))
	{
		var bFormatAsDate=false;
		if(propExists(jsonAxis,"DisplayAsDate"))
		{
			bFormatAsDate=jsonAxis.DisplayAsDate;
		}
		axis.SetDataFormat(jsonAxis.DataFormat,bFormatAsDate);
	}
	if(propExists(jsonAxis,"TickMark"))
		axis.SetTickMark(ChartAxisTickMarkFromString(jsonAxis.TickMark));

	if(propExists(jsonAxis,"CrossType"))
		axis.SetCrossType(ChartAxisCrossTypeFromString(jsonAxis.CrossType));

	if(propExists(jsonAxis,"DisplayUnits"))
		axis.SetDisplayUnits(jsonAxis.DisplayUnits);

	if(propExists(jsonAxis,"MajorGridLines"))
		axis.ShowMajorGridLines(jsonAxis.MajorGridLines);

	if(propExists(jsonAxis,"MajorUnitIntervalInterlacing"))
		axis.EnableMajorUnitIntervalInterlacing(jsonAxis.MajorUnitIntervalInterlacing);

	if(propExists(jsonAxis,"FixedDisplayRange"))
	{
		var axisRange = jsonAxis.FixedDisplayRange;
		if(!propExists(axisRange,"Lower"))
		{
			Session.Output("Lower attribute missing for FixedDisplayRange on axis" + jsonAxis.Label);
		}
		else if(!propExists(axisRange,"Upper"))
		{
			Session.Output("Upper attribute missing for FixedDisplayRange on axis" + jsonAxis.Label);
		}
		else
		{
			axis.SetFixedDisplayRange( axisRange.Lower, axisRange.Upper);
		}
	}
}


function SetChartAxes( chart, axes)
{
	for(var nAxis=0; nAxis < axes.length; nAxis++)
	{
		var jsonAxis = axes[nAxis];
		if(propExists(jsonAxis, "Index"))
		{
			// properies via chart
			var index = ChartAxisTypeFromString(jsonAxis.Index);
			if(propExists(jsonAxis, "IntervalInterlacing"))
			{
				if(jsonAxis.IntervalInterlacing)
				{
					chart.ShowAxisIntervalInterlacing(index);
				}
			}
			axis = chart.GetChartAxis( index );
			if(axis)
			{
				DefineAxis( axis, jsonAxis);
			}
			if(propExists(jsonAxis, "Visible"))
			{
				chart.ShowAxis( index, jsonAxis.Visible, true);
			}
		}
	}
	
	// process related axes
	for(var nAxis=0; nAxis < axes.length; nAxis++)
	{
		var jsonAxis = axes[nAxis];
		if(propExists(jsonAxis, "Source"))
		{
			var index = ChartAxisTypeFromString(jsonAxis.Source);
			axis = chart.GetChartAxis( index );
			if(axis==null)
			{
				Session.Output("Invalid source axis specified " + jsonAxis.Source);
			}
			else if(!propExists(jsonAxis, "Percent"))
			{
				Session.Output("Percent attribute missing for axis " + jsonAxis.Label);
			}
			else
			{
				var axisFlags=0;
				var bAtTop = false;
				var gap = 1;
				if(propExists(jsonAxis,"DisplayAbove"))
				{
					bAtTop = jsonAxis.DisplayAbove;
				}
				if(propExists(jsonAxis,"Gap"))
				{
					gap = jsonAxis.Gap;
				}
				var childAxis = axis.Split( jsonAxis.Percent, gap, bAtTop, axisFlags);
				if(childAxis)
				{
					relatedAxis[ jsonAxis.Label ] = childAxis;
					DefineAxis( childAxis, jsonAxis);
					if(propExists(jsonAxis, "Visible"))
					{
						childAxis.Visible=jsonAxis.Visible;
					}
				}
			}
		}
	}
}

function SetSeriesStyle( series, jsonStyle)
{
	var style  = series.GetSeriesFormat();
	if(style)
	{
		if(propExists(jsonStyle, "CurveType"))
		{
			style.SetCurveType( ChartCurveTypeFromString( jsonStyle.CurveType ) );
		}
		if(propExists(jsonStyle, "OutlineDashStyle"))
		{
			style.SetSeriesOutlineDashStyle( ChartDashStyleFromString( jsonStyle.OutlineDashStyle ) );
		}
		if(propExists(jsonStyle, "LineWidth"))
		{
			style.SetSeriesLineWidth( jsonStyle.LineWidth);
		}
	}
}

function SetChartSeries( chart, seriesArray)
{
	for(var nSeries=0; nSeries < seriesArray.length; nSeries++)
	{
		jsonSeries = seriesArray[nSeries];
		
		if(!propExists( jsonSeries, "Label")) {
			Session.Output("Label attribute missing for chart series");
			return false;
		}
		if(!propExists( jsonSeries, "Data")) {
			Session.Output("Data attribute missing for chart series");
			return false;
		}
		if(propExists( jsonSeries, "Category")) 
		{
			var chartType = ChartType.SIMPLE();
			if(propExists( jsonSeries, "Type")) 
			{
				chartType = ChartTypeFromString(jsonSeries.Type);
			}
			var color = ChartColor.Default();
			if(propExists(jsonSeries,"Color"))
			{
				color = jsonSeries.Color;
			}
			series = chart.CreateSeriesEx( jsonSeries.Label, color, chartType, ChartCategoryFromString(jsonSeries.Category));
		}
		else
		{
			series = chart.CreateSeries(jsonSeries.Label);
		}
		
		if(series)
		{
			if(propExists(jsonSeries,"StockSeriesType"))
				series.SetStockSeriesType(ChartStockSeriesTypeFromString(jsonSeries.StockSeriesType));
			if(propExists(jsonSeries,"Style"))
				SetSeriesStyle( series, jsonSeries.Style);
			if(propExists(jsonSeries,"Group"))
				series.SetGroupID(jsonSeries.Group);
			if(propExists(jsonSeries,"LevelRangeMode"))
				series.SetLevelRangeMode( ChartLevelRangeModeFromString(jsonSeries.LevelRangeMode));
			if(propExists(jsonSeries,"FrameStyle"))
				series.SetFrameStyle(ChartFrameStyleFromString(jsonSeries.FrameStyle));
			if(propExists(jsonSeries,"WireFrame"))
				series.SetWireFrame(jsonSeries.WireFrame);
			if(propExists(jsonSeries,"ColorMapCount"))
				series.SetColorMapCount(jsonSeries.ColorMapCount);
			if(propExists(jsonSeries,"ColorMode"))
				series.SetColorMode(ChartColorModeFromString(jsonSeries.ColorMode));
			if(propExists(jsonSeries,"SurfaceType"))
				series.SetSurfaceType(ChartSurfaceTypeFromString(jsonSeries.SurfaceType));
			if(propExists(jsonSeries,"DrawFlat"))
				series.SetDrawFlat(jsonSeries.DrawFlat);
			if(propExists(jsonSeries,"FrameColor"))
			{
				if(jsonSeries.FrameColor=="Default")
					series.SetFrameColor(ChartColor.Default());
				else
					series.SetFrameColor(jsonSeries.FrameColor);
			}	
			if(propExists(jsonSeries, "FitDiagramArea"))
				series.EnableFitDiagramArea( jsonSeries.FitDiagramArea);
		
			if(propExists(jsonSeries, "FillGradientType"))
				series.SetDefaultFillGradientType( ChartGradientTypeFromString(jsonSeries.FillGradientType));
		
			if(chartLegendDescriptor.bLegend)
				series.SetLegendLabelContent(chartLegendDescriptor.nValue);
			
			var jsonSeriesData = jsonSeries.Data;
			switch(jsonSeriesData.Type)
			{
				case "Pie":
				{
					for(var e = 0; e < jsonSeriesData.Points.length; e++)
					{
						var dp = jsonSeriesData.Points[e];
						if(!propExists(dp, "Y"))
							Session.Output("Missing Y value for data point, series:" + jsonSeries.Label);
						else if(!propExists(dp, "Category"))
							Session.Output("Missing Category name for data point, series:" + jsonSeries.Label);
						else
							chart.AddChartData( dp.Category, dp.Y, nSeries);
					}
					break;
				}
				case "YXZ":
				{
					for(var e = 0; e < jsonSeriesData.Points.length; e++)
					{
						var dp = jsonSeriesData.Points[e];
						if(!propExists(dp, "Y"))
						{
							Session.Output("Missing Y attribute for data point, series:" + jsonSeries.Label);
						}
						else if(!propExists(dp, "X"))
						{
							Session.Output("Missing X attribute for data point, series:" + jsonSeries.Label);
						}
						else if(!propExists(dp, "Z"))
						{
							Session.Output("Missing Z attribute for data point, series:" + jsonSeries.Label);
						}
						else
						{
							chart.AddChartDataYXZ( dp.Y, dp.X, dp.Z, nSeries);
						}
					}
					break;
				}
				case "Column":
				{
					for(var e = 0; e < jsonSeriesData.Points.length; e++)
					{
						var dp = jsonSeriesData.Points[e];
						if(!propExists(dp, "Category"))
						{
							Session.Output("Missing Category attribute for data point, series:" + jsonSeries.Label);
						}
						else if(propExists(dp,"Y"))
						{
							if(propExists(dp, "Y1"))
								chart.AddChartDataYY1( dp.Category, dp.Y, dp.Y1, nSeries);
							else 
								series.AddDataPoint3( dp.Category, dp.Y);
						}
					}
					break;
				}
				case "Stock":
				{
					for(var e = 0; e < jsonSeriesData.Points.length; e++)
					{
						var dp = jsonSeriesData.Points[e];
						var dt = new Date(dp.Time);
						series.AddStockData( dp.Open, dp.High, dp.Low, dp.Close, dt.getTime());
					}
					break;
				}
				case "Normal":
				{
					for(var e = 0; e < jsonSeriesData.Points.length; e++)
					{
						var dp = jsonSeriesData.Points[e];
						if(propExists(dp, "X") && propExists(dp,"Y"))
							series.AddDataPoint2( toDouble(dp.Y), toDouble(dp.X) );
						else if(propExists(dp,"Y"))
							series.AddDataPoint( toDouble(dp.Y) );
					}
					break;
				}
				case "Box":
				{
					for(var e = 0; e < jsonSeriesData.Points.length; e++)
					{
						var dp = jsonSeriesData.Points[e];
						series.AddBoxPlotData( dp.Average, dp.Min, dp.Q1, dp.Q2, dp.Q3, dp.Max, dp.Notched);
					}
					break;
				}
			}
			if(propExists( jsonSeries, "RelatedAxis"))
			{
				var related = jsonSeries.RelatedAxis;
				if(propExists(related,"Label"))
				{
					var raxis = relatedAxis[related.Label];
					if(raxis)
					{
						series.SetRelatedAxis( raxis.GetGuid(), ChartAxisIndexFromString(related.Index));
						relatedAxis[related.Label] = null;
					}
				}
			}
			if(propExists(	jsonSeries, "Shape"))
			{
				var shape = jsonSeries.Shape;
				series.CloseShape(shape.Close,shape.Fill);
			}				
		}
	}
	return true;
}

function ConstructChartFromJSON( chartGuid, jsonObj)
{
	var chartElement  as EA.Element;
	var chart as EA.Chart;
	
	chart=null;
	chartElement = GetElementByGuid( chartGuid );
	if(chartElement)
		chart = chartElement.GetChart();
	
	if(chart== null) {
		Session.Output("failed to get chart element !");
		return false;
	}		
	if(jsonObj == null) {
		Session.Output("failed to get parse JSON for chart !");
		return false;
	}	
	if(!propExists( jsonObj, "Series"))
	{
		Session.Output("No series data present JSON input!");
		return false;
	}		
	var jsonSeries = jsonObj.Series;

	if(!SetChartAttributes(chart,jsonObj))	{
		Session.Output("failed to define chart attributes!");
		return false;
	}
	// Stock series requires axis established before series
	if(propExists( jsonObj, "Axis")) {
		SetChartAxes(chart,jsonObj.Axis);
	}		
	if(!SetChartSeries(chart,jsonSeries)){
		Session.Output("failed to define chart series!");
		return false;
	}

	// we do this after creating series, as setting label options will
	// filter through to series at same time
	if(propExists( jsonObj,"DataLabels"))
	{
		var dataLabels = jsonObj.DataLabels;
		var labelOptions = chart.GetDataLabelOptions();
		if(propExists( dataLabels, "Position"))
			labelOptions.Position = ChartLabelPositionFromString( dataLabels.Position );
		if(propExists( dataLabels, "Underline"))
			labelOptions.Underline = dataLabels.Underline;
		if(propExists( dataLabels, "Content"))
			labelOptions.Content = ChartLabelContentFromString(dataLabels.Content);
	}
		
	chart.Redraw();
	
	return true;
}



var monthNames = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ];

function Rand(min, max) {
  min = cephes.ceil(min);
  max = cephes.floor(max);
  // drand returns 1.0 <= y < 2.0.
  return cephes.floor((cephes.drand()-1) * (max - min+1)) + min; //The maximum is exclusive and the minimum is inclusive
}

function fill3DChart( feature, chart)
{
	chart.Title = "Manhattan Stacked Chart in 3D";
	//pChart->SetLegendPosition(BCGPChartLayout::LP_NONE);

	var dgm3D = chart.GetDiagram3D();
	//dgm3D.SetExplicitGrouping(CBCGPChartDiagram3D::EG_NOT_GROUPED);

	for (var i = 0; i < 9; i++)
	{
		var series = chart.CreateSeries("");
		//pBarSeries->m_bIncludeSeriesToLegend = FALSE;
		for (var j = 0; j < 3; j++)
		{
			series.AddDataPoint( cephes.ceil(Rand(2.0, 15.0)));
		}
		series.SetGroupID(i / 3);
	}
}

function fill2DChart( feature, chart)
{
	var series1 as EA.ChartSeries;
	var series2 as EA.ChartSeries;
	var series3 as EA.ChartSeries;
	var series4 as EA.ChartSeries;
	var axisX as EA.ChartAxis;

	chart.Title = "Vehicle Expenses";
	axisY = chart.GetChartAxis( ChartAxisType.Y_PRIMARY_AXIS());
	axisY.SetAxisName( "Cost/$AUD (1:1000)",true);
	axisY.SetDataFormat("%.2f",false);
		
	series1 = chart.CreateSeries("Fuel");
	series2 = chart.CreateSeries("Taxes");
	series3 = chart.CreateSeries("Maintenance");
	series4 = chart.CreateSeries("Other");

	// fuels
	series1.AddDataPoint3( monthNames[0], 10.5);
	series1.AddDataPoint3( monthNames[1], 8.4);
	series1.AddDataPoint3( monthNames[2], 7.2);
	series1.AddDataPoint3( monthNames[3], 4.5);
	series1.AddDataPoint3( monthNames[4], 5.5);
	series1.AddDataPoint3( monthNames[5], 5.5);

	// taxes
	series2.AddDataPoint(1.4);
	series2.AddDataPoint(0.9);
	series2.AddDataPoint(0.5);
	series2.AddDataPoint(0.7);
	series2.AddDataPoint(0.8);
	series2.AddDataPoint(0.8);

	// maint
	series3.AddDataPoint(5);
	series3.AddDataPoint(7);
	series3.AddDataPoint(6);
	series3.AddDataPoint(4);
	series3.AddDataPoint(4);
	series3.AddDataPoint(6);

	// other
	series4.AddDataPoint(2);
	series4.AddDataPoint(3);
	series4.AddDataPoint(5);
	series4.AddDataPoint(3);
	series4.AddDataPoint(2);
	series4.AddDataPoint(2);

	if (feature == ChartFeature.StackedColumnSideBySide2D() || feature == ChartFeature.StackedBarSideBySide2D())
	{
		series1.SetGroupID(0);
		series1.SetGroupID(0);
		series3.SetGroupID(1);
		series4.SetGroupID(1);
	}
}

function ConstructChartForFeature( chartGuid, feature )
{
	var chart as EA.Chart;
	var diagram as EA.ChartDiagram3D;
	var element = GetElementByGuid(chartGuid);
	chart = element.GetChart();

	var chartCategory = ChartCategory.Column();
	var chartType = ChartType.SIMPLE();

	switch(feature)
	{
		case ChartFeature.ClusteredBar3D():
		case ChartFeature.StackedBarSideBySide3D():
		{
			chartCategory = ChartCategory.Bar3DSmart();
			break;
		}
		case ChartFeature.ClusteredBar2D():
		case ChartFeature.StackedBarSideBySide2D():
		{
			chartCategory = ChartCategory.BarSmart();
			break;
		}
		case ChartFeature.StackedBar2D():
		case ChartFeature.StackedBar1002D():
		{
			chartCategory = ChartCategory.Bar();
			break;
		}
		case ChartFeature.StackedBar1003D():
		case ChartFeature.StackedBar3D():
		{
			chartCategory = ChartCategory.Bar3D();
			break;
		}
		case ChartFeature.StackedColumn3D():
		case ChartFeature.StackedColumnManhattan3D():
		case ChartFeature.ClusteredColumn3D():
		{
			chartCategory = ChartCategory.Column3D();
		}
	}

	switch (feature)
	{
		case ChartFeature.StackedColumn2D():
		case ChartFeature.StackedBar2D():
		case ChartFeature.StackedColumnSideBySide2D():
		case ChartFeature.StackedBarSideBySide2D():
		case ChartFeature.StackedColumn3D():
		case ChartFeature.StackedBar3D():
		case ChartFeature.StackedColumnSideBySide3D():
		case ChartFeature.StackedBarSideBySide3D():
		case ChartFeature.StackedColumnManhattan3D():
		{
			chartType = ChartType.STACKED();
			break;
		}
		case ChartFeature.StackedColumn1002D():
		case ChartFeature.StackedBar1002D():
		case ChartFeature.StackedColumn1003D():
		case ChartFeature.StackedBar1003D():
		{
			chartType = ChartType.STACKED100();
			break;
		}
	}
	chart.SetChartType( chartCategory, chartType, false, true);
	
	if(feature == ChartFeature.StackedColumnManhattan3D())
	{
		fill3DChart( feature, chart);
	}
	else
	{
		fill2DChart( feature, chart);
	}
	chart.Redraw();
}
