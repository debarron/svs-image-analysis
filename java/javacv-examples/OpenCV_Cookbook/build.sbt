// @formatter:off

name         := "opencv-cookbook"
organization := "javacv.examples"

val javacppVersion = "1.5.2"
version      := javacppVersion
scalaVersion := "2.13.1"
scalacOptions ++= Seq("-unchecked", "-deprecation", "-Xlint")

// Platform classifier for native library dependencies
val platform = org.bytedeco.javacpp.Loader.getPlatform
// Libraries with native dependencies
val bytedecoPresetLibs = Seq(
  "opencv" -> s"4.1.2-$javacppVersion",
  "ffmpeg" -> s"4.2.1-$javacppVersion",
  "openblas" -> s"0.3.7-$javacppVersion"
).flatMap {
  case (lib, ver) => Seq(
    // Add both: dependency and its native binaries for the current `platform`
    "org.bytedeco" % lib % ver withSources() withJavadoc(),
    "org.bytedeco" % lib % ver classifier platform
  )
}

libraryDependencies ++= Seq(
  "org.bytedeco"            % "javacpp"         % javacppVersion withSources() withJavadoc(),
  "org.bytedeco"            % "javacv"          % javacppVersion withSources() withJavadoc(),
  "org.scala-lang.modules" %% "scala-swing"     % "2.1.1",
  "junit"                   % "junit"           % "4.12" % "test",
  "com.novocode"            % "junit-interface" % "0.11" % "test"
) ++ bytedecoPresetLibs

resolvers += "Sonatype OSS Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots"
resolvers += Resolver.mavenLocal

autoCompilerPlugins := true

// fork a new JVM for 'run' and 'test:run'
fork := true
// add a JVM option to use when forking a JVM for 'run'
javaOptions += "-Xmx1G"


assemblyMergeStrategy in assembly := {
 case PathList("META-INF", xs @ _*) => MergeStrategy.discard
 case x => MergeStrategy.first
}


// Set the prompt (for this build) to include the project id.
shellPrompt in ThisBuild := { state => "sbt:" + Project.extract(state).currentRef.project + "> " }
