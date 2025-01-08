case class ColoredPoint(x: Int, y: Int, c: String)
class RedPoint(x: Int, y: Int) extends ColoredPoint(x, y, "red")
class GreenPoint(x: Int, y: Int) extends ColoredPoint(x, y, "green")

val colored = ColoredPoint(0, 0, "red")
val red1 = new RedPoint(0, 0)
val red2 = new RedPoint(0, 0)
val green = new GreenPoint(0, 0)

/*
 * Why? `equals` method from parent class is called?
 */
red1 equals colored // true
red2 equals colored // true
red1 equals red2 // true

red1 == colored // true
red2 == colored // true
red1 == red2 // true

colored equals green // false
red1 equals green // false
red2 equals green // false

colored == green // false
red1 == green // false
red2 == green // false
