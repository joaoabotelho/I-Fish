# I-Fish

We transformed the common **Big Mouth Billy Bass (BMBB) into an inteligent fish** that responds accordingly to your questions.
This is the code behind this project and a **simulator that mymics the mouth of the fish**.

## Getting Started

The main code it's for the fish it self, for that you will need a BMBB and to follow our [hardware instructions]().
If you only want to see our **analysis** of audio working we have a **simulation** working get the code on [this directory](https://github.com/joaoabotelho/I-Fish/tree/master/simulator)

### Installing

First install `SpeechRecognition`, `apiai`, `gTTS`, `numpy` and `pygame`
```
$ pip3 install SpeechRecognition apiai gTTS numpy pygame
```

If you want the simulaton working you will also need to install `matplotlib`, `peakutils` and `scikit-learn` 
```
$ pip3 install scikit-learn peakutils matplotlib 
```

## Transformation from sound wave to mouth movement

In our file `audio_analytics.py` you can give an input of audio to analysis, returning the positions over time of the mouth seen in the simulation and the BMBB.
For more information go to [our blogpost]().

## Running the simulator

Go to the [simulator directory](https://github.com/joaoabotelho/I-Fish/tree/master/simulator) and run
```
$ python mouth_sim.py
```

## Running BMBB

If you want to create your own inteligent fish go to [our blogpost]() for more information, where we have our history since the start of our idea, everything behind the code explained, future implementations and the construction of our fellow fish from start to the finished project.

## Authors

* [João Botelho](https://github.com/joaoabotelho) - Project Manager/Software Developer
* [Tiago Martins](https://github.com/tmartins1) - Software Developer
* [Filipe Lopes](https://github.com/erbarbar) - Hardware Developer
* [Diogo Isidoro](https://github.com/diogo8) - Software Developer
