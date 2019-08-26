# Using the Vision AI Developer Kit for Audio

## Overview

This repo demonstrates how to use the Vision AI Developer Kit (VAI DevKit) to develop a Neural Network model to process audio sounds.  For information on using Vision on the VAI DevKit, refer to [Vision AI DevKit main page](http://aka.ms/visionaidevkit).

## Background

Processing video or images through a Neural Network involves converting images, most commonly JPEG, into a NumPy array where features can be extracted and calculated.  At the hightest level, most Vision AI projects include this with added capabilities.

A few of the challenges with Vision include requiring a camera and the camera only has a limited field of view.  To detect images in a complete circle, you often need 4+ cameras, which has a higher cost and require specialized hardware to process so much data and networks.

Audio, using just a microphone, is a much more cost effective approach for lots of use cases.  The advantages of Audio include:
* Lower Price
* Full 360° coverage
* No dependency on light

While audio is not the answer to all use cases, it can be used in many.  With your eyes closed, listen to all the sounds around you and think about how you were "trained" to recognize the sound.

## Resources

* [Github Repository](http://aka.ms/) - this site
* [Azure Subscription](http://portal.azure.com) -- We will use Azure IoT Edge and Azure Machine Learning Workspace in the sample
* [Visual Studio Code](http://aka.ms/vscode) -- the IDE for this sample
* [Audio Documentation](http://aka.ms/) - all documentation for using the VAI DevKit for audio processing
* [Sample](http://aka.ms/) - a sample solution for audio processing on the VAI DevKit
* [Qualcomm QCS603](https://www.qualcomm.com/products/vision-intelligence-300-platform) - learn more about the chipset powering the Vision AI Developer Kit hardware

## Get a kit

You can purchase the DevKit from [Arrow Electronics](https://www.arrow.com/en/products/eic-ms-vision-500/einfochips-limited).
