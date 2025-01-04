import scala.util.Random

abstract class PL
case class Scala(creator: String, age: Int, version: Int) extends PL
case class Other(name: String, age: Int, version: Int) extends PL

val that =
  Random.shuffle(List(Scala("scala", 20, 3), Other("Any", 30, 22))).head

that match {
  case x: Scala         => x.age
  case Scala(_, age, _) => age - 15

  // It also works
  case lang @ Scala(_, age, _) if lang.version != 2 => age
  // matching for Scala with only 'scala' name ... it works
  case lang @ Scala(_, _, 2) => lang.age

  /*
   * The following two cases wouldn't work and failed to compile
   */
  /* want to match Other type */
  // case lang @ Other => ???
  /* matching for language with only version 2. */
  // case lang: Scala(_, _, 2) => ???

  // While using `@` symbol, the right side is an unapplied Instance
  case lang @ Other(_, _, _) => lang.age + 10
  // While using `:` symbol, the right side is a type
  case lang: Other => lang.age + 10

  case _ => 0
}
