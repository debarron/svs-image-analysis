name := "java-opencv-example"

version := "0.1"

scalaVersion := "2.11.12"

libraryDependencies ++= Seq(
  "org.bytedeco" % "javacpp" % "1.4.4",
  "org.bytedeco" % "javacv" % "1.4.4",
  "org.bytedeco.javacpp-presets" % "opencv" % "4.0.1-1.4.4" ,
  "org.bytedeco.javacpp-presets" % "opencv" % "4.0.1-1.4.4"  classifier "macosx"
)