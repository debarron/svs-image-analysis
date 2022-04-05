
name := "imageJExample"
scalaVersion := "2.11.8"

libraryDependencies ++= Seq( 
  "net.imagej" % "ij" % "1.52n"
)

assemblyMergeStrategy in assembly := {
 case PathList("META-INF", xs @ _*) => MergeStrategy.discard
 case x => MergeStrategy.first
}
