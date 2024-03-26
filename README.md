# PX4-Lab

# Secure Autonomous Systems


## Objective

There are multiple flight firmwares with different architectures and design principles, but understanding one of them helps with understanding others. In this project, we will delve into PX4 autopilot, an open-source autopilot firmware. The following objectives are designed to help you familiarize yourself with flight controller firmware:

1. **Install and use PX4** and PX4 Software-In-The-Loop simulator to perform quadrotor flight simulation.
2. **Gain familiarity with MAVLink** and controlling the UAV using offboard control.
3. **Understand the internals** of PX4 and uORB middleware.

After familiarizing ourselves with PX4, we will focus on **Man-In-The-Middle attacks on PX4**. We will implement a Man-In-The-Middle (MitM) attack on the PX4 firmware.

## Prelude

The usage of drones is gaining popularity: from agricultural usage to a more safety critical usage such as firefighting and search and rescue. Therefore, MP2 will focus on a auto-pilot flight controller. There are two popular opensource auto-pilot flight controller: PX4 and Ardupilot. Despite the architectural difference between the two, they both rely on the usage of a middleware to exchange messages between their components. In this MP, we will be using PX4 and its Software-In-The-Loop (SITL) flight controller simulation with Gazebo physics simulation.

  1. PX4 is a popular opensource autopilot that controls multicopters, fixed-wing aircrafts, rovers and submarines.
  ![image](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/dc45e6c0-2146-47ec-a733-5e40befe0e23)
  As shown in the diagram, PX4 is composed of modules and the modules communicate using the uORB middleware.
  2. uORB middware is a publish-subscribe middleware where a module can publish certain message topics and other modules can subscribe to the topic to get the message.
  3. PX4 provides Software-In-The-Loop(SITL) simulation platform where PX4 controls a simulated vehicle in the host machine.
     ![image](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/0898245e-7835-4f08-80b4-9ce591ca12fc)
  4. By default, SITL provides simplistic physics simulation. However, it supports Gazebo for more complex simulation.
  5. PX4 also provides Hardware-In-The-Loop where the environment is simulated in the host machine but the flight controller runs in the flgiht hardware.

Middleware, also called Data Distribution Service (DDS), is an integral part in autonomous vehicles. The middleware we have explored is uORB which is used by PX4 autopilot.

There also exists Ardupilot, another autopilot software, which uses Robotic Operating System (ROS) as middleware. uORB is similar to the original ROS since they follow the publish/subscribe paradigm.

Because application of these middleswares are safety-critical in nature, there are some security concerns since both were not initially designed with security in mind. ROS2, a newer standard of ROS with major changes, which was released (late 2010s) follows a DDS security specification The specification allows authentication, authorization, and encryption.

Therefore, in this MP, we will investigate why such security measures are necessary by performing MitM by hijacking a uORB topic. We assume the adversary (you) can deploy its malicious module into PX4 and can slightly change particular module of the firmware(specifically the EKF module).

## Setting up PX4
We prepared a VM image which has the PX4 setup. The setup has the following system requirement:
1. **13GB** Storage
2. **At least** 4GB memory
3. **VirtualBox/VMWare** (Note: Virtual Machines do not work very well with Apple M1/2 Macs, therefore it's advised to use an Intel Based Machine.)

To setup, download the VM image from here. The username and password for the VM image is <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">student</kbd>


## Running the PX4-SITL
**Running the simulator**
1. Download the VM image here.

2. Inside the VM, change the directory to the PX4: <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> cd /home/student/Desktop/MP2/PX4-Autopilot/</kbd>

3. To compile and start the simulation run: <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> make px4_sitl gazebo </kbd>

![image](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/39a424a7-e48d-419e-b412-c1ecc04b8cde)

4. In PX4 command prompt, start the mp2 module <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> mp2 start </kbd>

![module_running](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/ef02a893-3783-4553-a44d-2783e827aca3)

5. In another terminal, change the directory to MP2 base directory:  <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> cd /home/student/Desktop/MP2/PX4-Autopilot/ </kbd>

6. If the run is successful, you should see the following:

![gazebo_running](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/c1dcac37-aa05-4ddd-aac3-daf45c1b7466)

7. In another terminal, change the directory to the MP2 base directory and run the offboard control:  <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">  python3 mp2_offboard_control.py </kbd>

![offboard_control_running](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/3d244c24-67a5-4060-9c25-c14e0caf4f13)

## MP II Instructions

**1. Mavlink and Offboard Control**

Mavlink is the messaging protocol used by UAVs and rovers which contains information regarding the sensor data, state of the vehicle, and status of the vehicle.
-  The protocol also contains commands to control the vehicle.
-  Offboard control is a method of controlling the UAV like a script.
-  For instance, the offboard control script can command the vehicle to move up by a meter or maintain certain velocity or attitude.
-  In this MP, we will be using MAVSDK-Python and the script is located in <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> ~/Desktop/MP2/mp2_offboard_control.py </kbd>  
-  Check out the example script to implement the missions.
-  Also checkout the API documentation.
- Implement linear mission
  
      1. Place the setpoint to 10 meters above the ground for takeoff.
      2. Laterally move the vehicle by placing a position setpoint anywhere in the same altitude.
      3. Land where the vehicle was moved to.

2.

  -  When the script ends, the script outputs <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> traj.npy  </kbd>  in numpy format.
  - To read the data, use <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">numpy.load()  </kbd>.
  - The data is a matrix in following shape <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">(# of logs, 6)  </kbd>  where columns consists of (north_pos, east_pos, down_pos, north_vel, east_vel, down_vel).
  - Because the coordinates are in North, East, Down (NED) format, when the drone takes off, the down_pos value should be negative and decrease.
  - We provided a script which can run with the following command <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">python3 mp2_plot_traj.py  </kbd>.
  - The script creates a window with a 3D plot which can be rotated using mouse can the plot can be saved using the save icon.
    
    ![example_plot](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/4f8568e5-fefe-437b-8697-809351fdaaed)

  - The red and blue points represent the starting point of the log and the end points of the log respectively (i.e., the vehicle moved from red point to the blue point following the line).
  - The blue point does not need to reach the ground since it only implies that the logging ended before the vehicle fully landed.
  - However, Make sure that the vehicle reaches the position before sending out the next command.
  - To read the latest position, use <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> async with lock  </kbd> : and read from the variable <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> velpos  </kbd>.

  **3. uORB: Understanding the middleware**

  - We provided our skeleton module located in <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> PX4-Autopilot/src/modules/mp2  </kbd>. However, it needs to subscribe to the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> vehicle_local_position  </kbd>. You must uncomment /* and */.
  - To subscribe to the topic, use <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> orb_subscribe(ORB_ID(INSERT_TOPIC_NAME_HERE))  </kbd> to get the subscription id.
  - Poll for the topic using <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> px4_poll()  </kbd>.
  - If the polling recieves the topic of interest, the data can be read by first creating the struct to hold the data: <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> struct INSERT_TOPIC_NAME_s topic_msg  </kbd>.
  - For example, to create a struct variable to hold the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">sensor_gyro</kbd>  message, use <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> struct sensor_gyro_s var_name  </kbd>.
  - Copy the data to the struct using <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> orb_copy(topic id, subscription id, reference to struct) </kbd>  (e.g., for <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> sensor_gyro  </kbd> , it would be <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> orb_copy(ORB_ID(sensor_gyro), gyro_sub_id, &var_name);  </kbd>.
  - Check out this link for a more indepth tutorial. Therefore for this task, subscribe to that topic and have the position information print out using <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> PX4_INFO() </kbd>  which takes input like <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> printf()  </kbd>.
  
## 4.Man-In-The-Middle

For this section:
  - We will hijack a topic by creating a custom uORB topic and causing the EKF module to publish to the malicious topic than the true topic.
  - EKF module will be publishing under a malicious uORB topic.
  - MP2 module will subscribe to the malicious topic and publish under the true topic with spoofed values.
  - We will look into four types of spoofing: constant offset, random offset, rotated, and scaled.


**A. Adjustments in Running the PX4-SITL**
For this section, there is an extra step where you have to run a server script. There are additional files which you must download from here which contains the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">  mp2_server.py  </kbd>  and <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> mp2_lib  </kbd>. Later instructional steps will describe where to correctly extract the additional files.

**Running the simulator**

1. Start with the MP2 base directory: <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">cd /home/student/Desktop/MP2  </kbd> 

2. Run the MP2 server: <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">python3 mp2_server.py  </kbd>  which should wait for the mp2 module in the PX4 to run
   
![mp2_server_running](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/c3309c62-b305-4888-8f9e-634a05644eed)

4. In another terminal, change the directoy to <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">  cd /home/student/Desktop/MP2/PX4-Autopilot  </kbd>

5. Compile and start the simulation by running: <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> make px4_sitl gazebo  </kbd>
   
![px4_running (1)](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/fb68e920-c873-4dab-b674-6ed4fe94e98e)

7. In PX4 command prompt, start the mp2 module <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> mp2 start  </kbd>
   
![module_running (1)](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/8cf0b0b8-5022-410a-802a-aa1adf32e59b)

9. In the third terminal, change the directory to the MP2 base directory and run the offboard control: <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> python3 mp2_offboard_control.py  </kbd>
    
 ![offboard_control_running (2)](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/188b6837-f77d-4997-be4a-2bd511879eec)

**B. Implementation Steps**
    
1. Create a custom message that has the same structure as the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> vehicle_local_position  </kbd> under a different name.

a. Go to the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> msg  </kbd> in <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> PX4-Autopilot  </kbd> directory

b. Copy the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> vehicle_local_position.msg  </kbd>  under a different name of your choosing.

c. We will refer to it as <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> vehicle_local_position_copy  </kbd> 

d. At the bottom of the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> vehicle_local_position.msg  </kbd> , there should be two commented out lines
   
     ![msg_1](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/315322c2-7282-4aa3-ab48-aea0f0ae6c2b)

e. The commented out lines are responsible for it will be declared in <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> #inlcude  </kbd>.

f. Therefore, modify <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> vehicle_local_position_copy.msg  </kbd>  to make it distict from the original.
   ![msg_2](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/cbe394e5-f0e5-439d-b670-96adfa97274b)

g. Modify the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">msg/CMakeLists.txt  </kbd>  by adding <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> vehicle_local_position_copy.msgt  </kbd>  to <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> set(msg_files)  </kbd>.

3. Hijack the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> vehicle_local_position topic  </kbd>.

a. We want to modify the EKF module so that it publishes under the malicious topic.

b. In side <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">PX4-Autopilot/src/modules/ekf2/  </kbd>  we need to modify the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> EKF2Selector.cpp  </kbd>  and <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">EKF2Selector.hpp  </kbd>.

c. In side <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">EKF2Selector.hpp  </kbd>, first include the new message <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">#include <uORB/topics/vehicle_local_position_copy.h> </kbd> 

d. Then find the line <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">uORB::Publication<vehicle_local_position_s> _vehicle_local_position_pub{ORB_ID(vehicle_local_position)};  </kbd>  which is responsible for publishing the topic.

e. Replace it with <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> uORB::Publication<vehicle_local_position_copy_s> _vehicle_local_position_pub{ORB_ID(vehicle_local_position_copy)};  </kbd>  to make the variable publish under different topic.

f. Go to the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> EKF2Selector.cpp </kbd>  and find the function <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> PublishVehicleLocalPosition()  </kbd>.

g. In the very last few lines of code, find the line where <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">_vehicle_local_position_pub </kbd>  is used, create a struct of the new malicious and copy the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> vehicle_local_position  </kbd>  struct to it using <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">memcpy()  </kbd>  

h. Should look like this:

![pub](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/e8fa9b73-b29f-4bd1-805c-67ee05db8723)


4. Make the mp2 module communicate with the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">mp2_server.py  </kbd>.

a. Download the additional files here which contains <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> mp2_server.py  </kbd>  and <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">mp2_lib.cpp   </kbd>   and <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> mp2_lib.h  </kbd>  
   
b. Extract the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">mp2_server.py  </kbd>   in the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> ~/Desktop/MP2/  </kbd>    directory.
   
c. Extract the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> mp2_lib.cpp  </kbd>   and <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">mp2_lib.h  </kbd>   in the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> ~/Desktop/MP2/PX4-Autopilot/src/modules/mp2  </kbd>  directory.
   
d. Modify the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">mp2.hpp  </kbd>   inside the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">modules/mp2  </kbd> . Include the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">mp2_lib.h  </kbd>   in <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> mp2.hpp </kbd>. Add the following line <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">Mp2Server * mp2server;  </kbd>   to the private section of the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">MP2  </kbd>   class.
   
![lib_inc](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/a3d6492b-86e3-47a0-a9eb-5759f30b234d)

e. Add <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">memcpy()  </kbd>  mp2_lib.cpp and <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">memcpy()  </kbd>  mp2_lib.h in<kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">memcpy()  </kbd>   CMakeLists.txt under SRC

f. Modify the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">memcpy()  </kbd>  mp2.cpp inside the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">memcpy()  </kbd>   modules/mp2 to read the new topic.

1. Initizlize the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">mp2server  </kbd>   in the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">MP2contructor  </kbd>  

![mp2_module_1](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/afeefd24-091a-4869-923d-9fe431d96a0a)

2. Subscribe to <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">vehicle_local_position_copy  </kbd>   instead of <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">vehicle_local_position  </kbd>   (refer to MP2 part A, remember to change the struct type as well)

3. Inside the <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">run()  </kbd>   function, use <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">mp2server.exfiltrate()  </kbd>   to send the subscribed data to the server and <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">mp2server.recieve()  </kbd> 
  to get the offset values back from the server.

![mp2_module_2](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/868c638c-80b7-4f4e-95b6-3a971bae1f24)

4. Create <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">vehicle_local_position  </kbd>   struct and <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;">memcpy()  </kbd> the subscribed data to the struct.

5. Add the values recieved from the server to the x, y, z position of the struct.

6. Create publishing id (similar to how there was subscribe id in part A) using <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> orb_advertise()  </kbd> 

7. Publish the topic using <kbd style="background-color: #f0f0f0; border: 1px solid #ddd; padding: 5px;"> orb_publish()  </kbd>  

   ![mp2_module_3](https://github.com/fakhruddinbabor7/px4_lab/assets/71979845/656b60f9-2f7a-4d6d-b335-97ef41342e7f)


4. Implement the attack types in the mp2_server.py

       a. Find the "TODO:" flags in the script and implement the corresponding attack.

       b. Fixed offset attack adds fixed constant value (of your choosing) to each of the position values (specify the value you used in the report).

       c. Random offset attack adds random value in a specified range (of your choosing) to each of the position values (specify the range of values you used in the report).

       d. Flipped attack causes move in a trajectory where the X and Y positions are flipped.

       e. Scaled attack causes move in a trajectory where the X and Y movements are scaled by a constant (i.e., if the mission is for the vehicle to move along x axis by 2 meters, in actualality it would move by 2*constant).

       f. The mp2_server.py outputs exfil_traj.npy which can be used by the prior plotting script by finding changing the "traj.npy" to "exfil_traj.npy".


Note: For each of the above missions, repeat them for the missions from the first section of this MP's Instructions, i.e. linear and circular.

Also, the "mission" is finite time and only should attack between the interval where drone takes off and stop when it lands.


   











