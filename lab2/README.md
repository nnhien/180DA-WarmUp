# Lab 2: MQTT and Speech Recognition

## MQTT
MQTT makes it possible to communicate with many devices at once. It is very easy to do a multicast transmission with MQTT. It is a little cumbersome to communicate to individual devices, since either we'd need to know the topic a particular client is subscribed to a priori, or we'd need to dynamically populate a list of available clients. I used a 1 second delay between messages and it seemed to perform as expected, so on that timescale the delay caused MQTT is insignificant.

## Speech Recognition
a. With this speech recognition program, we can do simple speech to text conversions. At the moment, I cannot detect aspects of the sound like pitch, timber, etc.

b. I probably want my group's speech recognition to be pretty simple. Likely we will just do single word recognition, even though the library can detect simple phrases.

c. We don't need very high accuracy, since we will probably be using speech recognition for menu commands or simple gameplay. If we follow through with the bomb game idea, inaccuracies will hurt the experience. This can be mitigated by choosing keywords which are distinct not only from each other but also from other words

d. If we wanted greater accuracy, we'd probably use a dedicated microphone. To have absolute confidence in the recognizer's performance, we'd need a relatively quiet environment. 
