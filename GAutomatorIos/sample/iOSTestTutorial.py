import random
import ga2
import cv2
import time
import logging
import ga2.cloud.reporter as reporter
from config import TestInfo,EngineType
logger = logging.getLogger("iOSTestTutorial")

'''
local test steps:
1. start your webdriveragent test project on device 
2.iproxy xxxxx 8100 device_udid
3. start to edit and run your code 
'''


'''
a sample to get device.engine instance 
'''
def random_travel(rounds=20):
    top_app = device.get_top_app()
    logger.info("current top  app: " + top_app)
    for i in range(rounds):
        time0 = time.time()
        current_scene = device.engine_connector().get_scene()
        if current_scene:
            logger.info("current scene:" + current_scene)
        uielements = device.engine_connector().get_touchable_uielements()
        print("get touchable elements cost: " + str(time.time() - time0))
        if not uielements:
            continue
        elem = random.sample(uielements, 1)[0]
        bound = elem.bound
        reporter.Reporter().screenshot()
        device.touch(bound.x + bound.width / 2, bound.y + bound.height / 2)
        time.sleep(1)


'''
a sample to find engine element
'''
def wait_test():
    elem = ga2.wait_element(ga2.By.NAME_IN_ENGINE, "/Canvas/Panel/Interaction")
    if elem is None:
        logger.error("element is not found")

'''
a sample to assert element exists
'''
def wait_fail_test():
    assert(ga2.wait_element(ga2.By.NAME_IN_ENGINE, "badboy",timeout=6))


'''
a sample to touch engine element
'''
def touch_test():
    ga2.touch_element(ga2.By.NAME_IN_ENGINE, "/Canvas/Panel/FindElements")


'''
a sample to get the screenshot
'''
def screenshot_test():
    image = device.screenshot()
    cv2.imwrite("test.jpg", image)

def test_multifingers():
    actions = [
        dict(x1=100, y1=200, x2=200, y2=200, dur=5000),
        dict(x1=100, y1=250, x2=200, y2=250, dur=5000),
        dict(x1=100, y1=300, x2=200, y2=300, dur=5000),
        dict(x1=100, y1=350, x2=200, y2=350, dur=5000)
    ]
    ga2.multi_fingers_swipe(ga2.By.NAME_IN_ENGINE,actions)

device = ga2.init_device(ga2.DeviceType.DEVICE_IOS, TestInfo.udid)  # get the instance of device
ga2.launch_app(TestInfo.PACKAGE)#if you are going to test a specific scene, just comment out this line.
ga2.init_engine_sdk(enginetype=EngineType)
test_multifingers()
wait_test()
touch_test()
random_travel()
screenshot_test()
wait_fail_test()
# device.iproxy.removeAllForwards()
