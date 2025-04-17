# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import configparser
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageFilter
import imagehash
from os import walk
import pandas as pd
import os
import time
import datetime
import subprocess
import shutil
from bblt.ocr_util import ocr
from bblt.appium_driver import AppiumDriver
file_dir = str(__file__).replace(str(__file__).split("/")[-1], "")


class launchtest:
    def __init__(self, run_times=10, different_allow=15, ios="http://localhost:8100"):
        print("Init parameters....")
        settings = configparser.RawConfigParser()
        settings.read('./settings.ini')
        self.dashboard_copy_list = settings['config']['dashboard_copy_list'].split(',')
        self.dashboard_copy_list_en = settings['config']['dashboard_copy_list_en'].split(',')

        self.times = run_times
        self.ios_host = ios
        self.package_name = ""
        self.device_os = ""
        self.device_id = ""
        self.different_allow = different_allow
        self.file_dir = str(__file__).replace(str(__file__).split("/")[-1], "")
        self.ocr = ocr()
        self.start_pix_difference = int(settings['config']['start_pix_difference'])
        self.start_ocr_verification = int(settings['config']['start_ocr_verification'])
        self.cut_image_num = int(settings['config']['cut_image_num'])
        self.videoFPS = int(settings['config']['videoFPS'])
        self.image_slot_time = 1/self.cut_image_num

    def init_file_directory(self, device_name):
        video_path = self.file_dir + f"/recorded_videoes/{device_name}/video"
        screenshot_path = self.file_dir + f"/recorded_videoes/{device_name}/screenshot"
        try:
            shutil.rmtree(path=video_path)
        except:
            pass
        try:
            shutil.rmtree(path=screenshot_path)
        except:
            pass
        self.mk_folder(dir=video_path)
        self.mk_folder(dir=screenshot_path)

    def start_android_screen_recording(self, video_path):
        global process_scrcpy
        command_linux = f"scrcpy --no-playback --no-window --record={video_path}"
        process_scrcpy = subprocess.Popen(command_linux, shell=True)
        pass

    def pause_android_screen_recording(self):
        time.sleep(10)
        if process_scrcpy is not None:
            subprocess.Popen.kill(process_scrcpy)

    def mk_folder(self, dir):
        self.set_print(f"Create folder: {dir}", style="6", color=33)
        try:
            os.stat(dir)
        except:
            os.makedirs(dir)

    def convert_video_to_screenshot(self, video_file, dir):
        screenshot_path = dir + "/%04d.jpg"
        command = "ffmpeg -i " + video_file + f"  -vf fps={self.cut_image_num} " + screenshot_path
        self.set_print(command, style="6", color=33)
        process_temp = subprocess.Popen(command, shell=True)
        process_temp.communicate()
        time.sleep(10)
        if process_temp is not None:
            subprocess.Popen.kill(process_temp)

    def cut_video_new(self, device_name):
        self.set_print(f"Start to cut video...")
        time.sleep(5)
        video_path = file_dir + "/recorded_videoes/" + device_name + "/video/"
        screen_path = file_dir + "/recorded_videoes/" + device_name + "/screenshot/"
        video_list = []
        self.set_print(f"Video Path: {video_path}", style="6", color=33)
        for (dirpath, dirnames, filenames) in walk(video_path):
            video_list.extend(filenames)
            break
        try:
            video_list.remove(".DS_Store")
        except:
            pass
        for video in video_list:
            video_folder = screen_path + video.replace(".mkv", "")
            converted_folder = video_folder + "/converted/"
            self.mk_folder(converted_folder)
            self.convert_video_to_screenshot(video_path + video, converted_folder)
        self.set_print(f"Calculate application launch time")
        self.show(device_name=device_name, different_allow=self.different_allow)
        self.set_print(f"Launch Time Test Finished")

    def crop_image(self, dir, size):
        f = []
        for (dirpath, dirnames, filenames) in walk(dir):
            f.extend(filenames)
            break
        for file in f:
            command = "convert " + dir + "/" + file + " -crop "+size+" " + dir + "/converted/" + file
            self.set_print(command, style="6", color=33)
            process_temp = subprocess.Popen(command, shell=True)
            process_temp.communicate()
            time.sleep(10)
            if process_temp is not None:
                subprocess.Popen.kill(process_temp)

    def get_dashboard_start_location_via_ocr(self, file_dir):
        image_lists = []
        image_list = os.listdir(file_dir)
        for item in image_list:
            image_lists.append(item)
        image_lists.sort()
        for f in image_lists:
            if int(f.replace(".jpg", "")) > self.start_ocr_verification:
                ocr_list = self.get_copy_list(file_dir + f)
                self.set_print(f"Picture: {f}", style="6", color=33)
                self.set_print(f"Picture Dashboard Copy: {ocr_list}", style="6", color=33)
                self.set_print(f"Picture Copy List: {self.dashboard_copy_list}", style="6", color=33)
                self.set_print(f"Picture Copy List en: {self.dashboard_copy_list_en}", style="6", color=33)
                if set(self.dashboard_copy_list) < set(ocr_list):
                    return f
                if set(self.dashboard_copy_list_en) < set(ocr_list):
                    return f
        return None

    def get_copy_list(self, image_dir):
        result = self.ocr.get_ocr_result_of_image(image_dir)
        try:
            copy_list = self.ocr.get_copy_list(result=result)
        except:
            copy_list = []
        return copy_list

    def show(self, device_name, different_allow):
        global dirnames_parent, dirpath_parent
        video_path = file_dir + "/recorded_videoes/"+device_name+"/screenshot/"
        for (dirpath_parent, dirnames_parent, filenames_parent) in walk(video_path):
            break
        differences = {}
        data = {}
        for line in dirnames_parent:
            dir = dirpath_parent + line + "/converted/"
            self.set_print(dir, style="6", color=33)
            file = []
            difference = []
            for (dirpath, dirnames, filenames) in walk(dir):
                file.extend(filenames)
            file.sort()
            file_num = 0
            end_file = self.get_dashboard_start_location_via_ocr(dir)
            for f in file:
                if f == end_file:
                    break
                img1 = Image.open(dir + f)
                img2 = Image.open(dir + file[file_num + 1])
                img1 = img1.filter(ImageFilter.BoxBlur(radius=3))
                img2 = img2.filter(ImageFilter.BoxBlur(radius=3))
                phashvalue = imagehash.phash(img1) - imagehash.phash(img2)
                ahashvalue = imagehash.average_hash(img1) - imagehash.average_hash(img2)
                totalaccuracy = phashvalue + ahashvalue
                if totalaccuracy < different_allow:
                    totalaccuracy = 0
                difference.append(totalaccuracy)
                self.set_print(f + " and " + file[file_num + 1] + " : " + str(totalaccuracy), style="6", color=33)
                file_num += 1
                if file_num == len(file) - 1:
                    break
            differences[line] = difference
        differences = self.mend_list(differences)
        xarray = []
        total_time = 0
        for diff in differences:
            start_point = 0
            for i in range(0, len(differences[diff])):
                if differences[diff][i] > self.start_pix_difference and start_point == 0:
                    start_point = self.image_slot_time * i
                    break
            launch_time = self.image_slot_time * int(f.replace(".jpg", "")) - start_point
            data[diff.split('.')[-1] + ": " + str(round(launch_time, 2)) + "(s)"] = differences[diff]
            total_time += launch_time

        for diff in differences:
            for i in range(0, len(differences[diff])):
                xarray.append(self.image_slot_time * i)
            break
        df = pd.DataFrame(data, index=xarray)
        df.cumsum()
        df.plot()
        plt.title("App Launch time in " + device_name + ": " + str(round(total_time/len(differences), 2)))
        plt.xlabel("App bblt image actions change")
        plt.ylabel("Launch time")
        file_location = file_dir + "/recorded_videoes/"+device_name + '.png'
        plt.savefig(file_location)
        plt.show()
        plt.close()

    def mend_list(self, li):
        len_list = []
        for item in li:
            len_list.append(len(li[item]))
        max_len = max(len_list)
        for item in li:
            for i in range(0, max_len-len(li[item])):
                li[item].append(0)
        return li

    def android_launch_scrspy(self, driver):
        device_name = driver.capabilities['deviceManufacturer'] + "_" + driver.capabilities['deviceModel']
        self.package_name = driver.capabilities['bundle_id']
        self.set_print(f"Android Device {device_name} Launch Time Test Started")
        self.init_file_directory(device_name)
        for x in range(0, self.times):
            start_time = str(datetime.datetime.now()).replace(" ", "_")
            video_path = file_dir + f"/recorded_videoes/{device_name}/video/video_{start_time}.mkv"
            try:
                driver.terminate_app(self.package_name)
            except:
                pass
            time.sleep(5)
            self.start_android_screen_recording(video_path)
            self.set_print(f"Start recording in: {video_path}")
            time.sleep(5)
            driver.activate_app(self.package_name)
            time.sleep(10)
            self.pause_android_screen_recording()
            driver.terminate_app(self.package_name)
            time.sleep(5)
            self.set_print(f"Finished round {x + 1} of {self.times} app launch")
        self.set_print(f"Android Launch Time Test Stopped")
        return device_name

    def ios_launch_appium(self, driver):
        device_name = driver.capabilities['deviceName'].replace(" ", "") + "_" + driver.capabilities['udid']
        self.package_name = driver.capabilities['bundle_id']
        self.set_print(f"IOS Device {device_name} Launch Time Test Started")
        self.init_file_directory(device_name)
        for x in range(0, self.times):
            start_time = str(datetime.datetime.now()).replace(" ", "_")
            video_path = file_dir + f"/recorded_videoes/{device_name}/video/video_{start_time}.mkv"
            try:
                driver.terminate_app(self.package_name)
            except:
                pass
            time.sleep(5)
            driver.start_recording_screen(videoFps=self.videoFPS)
            time.sleep(5)
            driver.activate_app(self.package_name)
            time.sleep(5)
            driver.terminate_app(self.package_name)
            video = driver.stop_recording_screen()
            with open(video_path, "wb") as fp:
                fp.write(base64.b64decode(video))
            try:
                driver.close()
            except:
                pass
            pass
            time.sleep(5)
            self.set_print(f"Finished round {x+1} of {self.times} app launch")
        self.set_print("IOS Launch Time Test Stopped")
        return device_name

    def launch_curve(self):
        driver = AppiumDriver().init_driver()
        self.device_os = driver.capabilities['platformName']
        if driver is None:
            return None
        if "ios" in self.device_os:
            device_name = self.ios_launch_appium(driver)
        else:
            device_name = self.android_launch_scrspy(driver)
        self.cut_video_new(device_name)

    def set_print(self, info, style="7", color=32):
        print(f'\033[{color};{style}m>>>>>>>>>>>>>> {info} \033[0m')

    def write_data_db(self):
        # #device os(ios/android), appversion, version_id, device_name, device_id, launchtime, times, environment, date
        # self.times = run_times
        # self.device_os = device_os
        # self.device_id = device_id
        #appversion 12.1
        #envrionment = "stage"
        pass


if __name__ == '__main__':
    #IOS
    #stage: com.disney.shanghaidisneyland.dev
    #prod: com.disney.shanghaidisneyland
    #Android
    #stage: com.disney.shanghaidisneyland_goo
    launchtest(run_times=1).launch_curve()
    # launchtest(package="com.disney.shanghaidisneyland_goo", device_os="android", run_times=10).launch_curve()
