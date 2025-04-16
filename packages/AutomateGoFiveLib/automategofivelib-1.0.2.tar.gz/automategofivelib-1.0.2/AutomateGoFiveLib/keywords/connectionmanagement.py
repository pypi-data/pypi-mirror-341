# -*- coding: utf-8 -*-

import robot
import inspect
import logging
import json
import requests

from appium import webdriver
from robot.libraries.BuiltIn import BuiltIn
from AutomateGoFiveLib.utils.applicationcache import ApplicationCache
from AppiumLibrary.keywords._logging import _LoggingKeywords

cache_app = BuiltIn()
method_cache_app = ApplicationCache()
log = _LoggingKeywords()

class ConnectionManagement:

    def __init__(self):
        #เนื่องจากปัญหาเรื่องโครงสร้าง structure เลยยังไม่สามารถใช้ได้
        # self._bi = BuiltIn()
        pass
    #KeyWord
    
    def native_close_application_session(self,alias=None):
        """Close Application And Quit Seesion

        =========================================================
        
        ปิดแอพปัจจุบันและปิดเซสชัน"""
        driver = self._current_application()
        log._debug('Closing application with session id %s' % self._current_application().session_id)
        method_cache_app.register(driver,alias)
        method_cache_app.close_all()

    def native_background_application(self, seconds=5):
        """
        Puts the application in the background on the device for a certain
        duration.

        =========================================================

        วางแอปพลิเคชันไว้ในพื้นหลังของอุปกรณ์เป็นระยะเวลาหนึ่ง.
        """
        self._current_application().background_app(seconds)
        
    def native_activate_application(self, app_id):
        """
        Activates the application if it is not running or is running in the background.
        Args:
         - app_id - BundleId for iOS. Package name for Android.

        New in AppiumLibrary v2

        =========================================================

        
        เปิดใช้งานแอปพลิเคชันหากมันไม่ได้รันอยู่หรือรันอยู่ในพื้นหลัง
        อาร์กิวเมนต์:
        - app_id - BundleId สำหรับ iOS, ชื่อแพ็คเกจสำหรับ Android.
        """
        self._current_application().activate_app(app_id)

    def native_terminate_application(self, app_id):
        """
        Terminate the given app on the device

        Args:
         - app_id - BundleId for iOS. Package name for Android.

        New in AppiumLibrary v2

        =========================================================
        
        ยุติแอปพลิเคชันที่กำหนดไว้บนอุปกรณ์แต่ยัง active อยู่ในระบบ
        สามารถเปิดต่อได้

        อาร์กิวเมนต์:  

        app_id - BundleId สำหรับ iOS, ชื่อแพ็คเกจสำหรับ Android.
        ใหม่ใน AppiumLibrary เวอร์ชัน 2
        """
        return self._current_application().terminate_app(app_id)
    
    def native_get_window_height(self):
        """Get current device height.

        Example:
        | ${width}       | Get Window Width |
        | ${height}      | Get Window Height |
        | Click A Point  | ${width}         | ${height} |

        New in AppiumLibrary 1.4.5
        """
        return self._current_application().get_window_size()['height']
    
    def native_get_window_width(self):
        """Get current device width.

        Example:
        | ${width}       | Get Window Width |
        | ${height}      | Get Window Height |
        | Click A Point  | ${width}          | ${height} |

        New in AppiumLibrary 1.4.5
        """
        return self._current_application().get_window_size()['width']
    
    def commond_install_app(self, app_path, app_package):
        """ *******Not available wait for update flutter*******
        Install App via Appium
        
        Android .

        - app_path - path to app (.apk)
        - app_package - package of install app to verify

        Ios .

        - app_path - path to app (.app | .ipa)
        - bundleId - package of install app to verify
        """
        driver = self._current_application()
        driver.install_app(app_path)
        return driver.is_app_installed(app_package)
    
    def get_source(self):
        """Returns the entire source of the current page.
        
        =========================================================

        ฟังก์ชันนี้จะส่งคืนสตริงที่มีซอร์สโค้ด HTML ของหน้าเว็บที่กำลังแสดงอยู่ในเบราว์เซอร์ในขณะนั้น 
        ซึ่งสามารถนำไปใช้ในการตรวจสอบหรือวิเคราะห์โครงสร้างหรือเนื้อหาของหน้าเว็บได้
        """
        return self._current_application().page_source
    
    def log_source(self, loglevel='INFO'):
        """Logs and returns the entire html source of the current page or frame.

        The `loglevel` argument defines the used log level. Valid log levels are
        `WARN`, `INFO` (default), `DEBUG`, `TRACE` and `NONE` (no logging).
        """
        ll = loglevel.upper()
        if ll == 'NONE':
            return ''
        else:
            if  "run_keyword_and_ignore_error" not in [check_error_ignored[3] for check_error_ignored in inspect.stack()]:
                source = self._current_application().page_source
                log._log(source, ll)
                return source
            else:
                return ''
            
    def get_driver(self):
        """*******Not available wait for update flutter*******
        Connect Session(Don't Create New Session & )
        """
        current_app_caps = self._current_application()
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_capabilities=current_app_caps, direct_connection=True)
        return driver
    

    def execute_script(self, script, **kwargs):
        """
        Execute a variety of native, mobile commands that aren't associated
        with a specific endpoint. See [https://appium.io/docs/en/commands/mobile-command/|Appium Mobile Command]
        for more details.

        Example:
        | &{scrollGesture}  |  create dictionary  |  left=${50}  |  top=${150}  |  width=${50}  |  height=${200}  |  direction=down  |  percent=${100}  |
        | Sleep             |  1                  |
        | Execute Script    |  mobile: scrollGesture  |  &{scrollGesture}  |

        Updated in AppiumLibrary 2
        """
        if kwargs:
            log._info(f"Provided dictionary: {kwargs}")

        return self._current_application().execute_script(script, kwargs)
    
    def get_appium_session_id(self):
        """Returns the current session ID as a reference"""
        log._info("Appium Session ID: " + self._current_application().session_id)
        return self._current_application().session_id
    
    #PRIVATE_FUNCTION
        
    def _current_application(self):
        """Return the instance of the current application
        From AppiumFlutterLibrary

        =========================================================

        คืนค่าอินสแตนซ์ของแอปพลิเคชันปัจจุบัน
        จาก AppiumFlutterLibrary
        """
        return cache_app.get_library_instance('AppiumFlutterLibrary')._current_application()
        # return self._bi.get_library_instance('AppiumFlutterLibrary')._current_application()

    def _get_platform(self):
        try:
            platform_name = self._current_application().desired_capabilities['platformName']
        except Exception as e:
            raise e
        return platform_name.lower()


        