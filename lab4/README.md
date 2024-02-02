MQTT response time: about 0.6s

Task 4:
    1. Gravity acceleration is present while idle
    2. The values drift when idle. The acceleration seems to be a good feature to detect idle versus non-idle.
    3. I used the x and z accelerometer axes. I used a decision tree based on a window of samples.
    4. I needed to use the x axis of the gyroscope to detect circular motion. It's not very easy to detect circular motion, since it requires a lot of sensor fusion to do anything more than one-axis rotation about the device. That is, to detect rotation about an arbitrary axis in space, a lot of sensor fusion would need to occur.