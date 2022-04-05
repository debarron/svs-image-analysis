package opencv_cookbook

import org.bytedeco.opencv.global.{opencv_imgcodecs => cvCoders}
import org.bytedeco.opencv.global.{opencv_imgproc => cvProc}
import org.bytedeco.javacpp.BytePointer
import org.bytedeco.opencv.opencv_core.MatVector
import org.bytedeco.opencv.opencv_core.Mat

import java.nio.file.{Files, Paths}

object Counters {

  def main(args:Array[String]):Unit = {

val path = args(0)
val bytes:Array[Byte] = Files.readAllBytes(Paths.get(path))
 
    val img = cvCoders.imdecode(new Mat(new BytePointer(bytes: _*)), cvCoders.IMREAD_UNCHANGED)
    val imgResult = new Mat 
    val contours = new MatVector
    
    cvProc.pyrMeanShiftFiltering(img, img, -10, 91) 
    cvProc.cvtColor(img, imgResult, cvProc.COLOR_BGR2GRAY)
    cvProc.threshold(imgResult, imgResult, 127, 255, cvProc.THRESH_BINARY_INV)
    cvProc.findContours(imgResult, contours, cvProc.RETR_LIST, cvProc.CHAIN_APPROX_SIMPLE)
    
    img._deallocate
    imgResult._deallocate
    
    println(s"${contours.size.toInt}")
  }
}


