import cv2 as cv
import os
import numpy as np
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
import rsp.common.color as color
import rsp.common.drawing as drawing

OS_NAMES = {
    'Linux': 'Linux',
    'Mac': 'Darwin',
    'Windows': 'Windows'
}

def __get_drives_windows__():
    drives = [ chr(x) + ":" for x in range(65,91) if os.path.exists(chr(x) + ":") ]
    return drives

def __get_drives_osx__():
    drives = os.listdir('/Volumes')
    for i, drive in enumerate(drives):
        drives[i] = f'/Volumes/{drive}'
    return drives

def __get_text_size__(text:str, fontScale, fontFace = cv.FONT_HERSHEY_SIMPLEX):
    ((fw,fh), baseline) = cv.getTextSize(
            text, fontFace=fontFace, fontScale=fontScale, thickness=1) # empty string is good enough
    return fh, fw

class UIElement():
    def __init__(
            self,
            label,
            px, py,
            w, h,
            fontScale = 0.4,
            on_left_button_clicked = None,
            on_left_button_released = None,
            focusable = True,
            is_enabled = True
        ):
        self.label = label
        self.__px__ = px
        self.__py__ = py
        self.__w__ = w
        self.__h__ = h
        self.__is_mouse_over__ = False
        self.__margin_inner__ = 1
        self.__margin_outer__ = 2
        self.__fontScale__ = fontScale
        self.__is_focused__ = False
        self.__on_left_button_clicked__ = on_left_button_clicked
        self.__on_left_button_released__ = on_left_button_released

        self.__focusable__ = focusable
        self.__is_enabled__ = is_enabled

    def __mouse_left_button_clicked__(self, x, y):
        if not self.__is_enabled__:
            self.__is_focused__ = False
            self.__is_mouse_over__ = False
            return
        if x >= self.__px__ and x <= self.__px__ + self.__w__ and \
            y >= self.__py__ and y <= self.__py__ + self.__h__:
            self.__is_focused__ = True
            if self.__on_left_button_clicked__ is not None:
                self.__on_left_button_clicked__()
        else:
            self.__is_focused__ = False

    def __mouse_left_button_released__(self, x, y):
        if x >= self.__px__ and x <= self.__px__ + self.__w__ and \
            y >= self.__py__ and y <= self.__py__ + self.__h__:
            if self.__on_left_button_released__ is not None:
                self.__on_left_button_released__()
        
    def __mouse_right_button_clicked__(self, x, y):
        pass

    def __mouse_moved__(self, x, y):
        if not self.__is_enabled__:
            self.__is_focused__ = False
            self.__is_mouse_over__ = False
            return
        if x >= self.__px__ and x <= self.__px__ + self.__w__ and \
            y >= self.__py__ and y <= self.__py__ + self.__h__:
            self.__is_mouse_over__ = True
            if isinstance(self, TextBox):
                pass
        else:
            self.__is_mouse_over__ = False

    def __draw__(self, img):
        if isinstance(self, TextBox):
            pass
        # focused border
        if self.__focusable__ and self.__is_focused__:
            img = cv.rectangle(img, (self.__px__ - self.__margin_inner__, self.__py__ - self.__margin_inner__), (self.__px__ + self.__w__ + self.__margin_inner__, self.__py__ + self.__h__ + self.__margin_inner__), color=color.FOCUSED, thickness=1)

        # mouse over border
        if self.__focusable__ and self.__is_mouse_over__:
            img = cv.rectangle(img, (self.__px__ - self.__margin_outer__, self.__py__ - self.__margin_outer__), (self.__px__ + self.__w__ + self.__margin_outer__, self.__py__ + self.__h__ + self.__margin_outer__), color=color.CORNFLOWER_BLUE, thickness=1)

    def __key_input__(self, key):
        pass

class TextBox(UIElement):
    def __init__(self, label, text, px, py, w = 50, check_valid = None, type = str, min = None, max = None):
        super().__init__(label, px, py, w, 20)
        self.text = str(text)
        self.value = text
        self.__enter_pressed__ = False
        self.__cursor_pos__ = len(self.text)
        self.__cursor_blink_interval__ = timedelta(milliseconds=1000)
        self.__cursor__ = '|'
        self.__last_blink_time__ = datetime.now()
        self.__type__ = type
        self.__min__ = min
        self.__max__ = max
        self.__check_valid__ = self.__cheeck_type_valid__ if check_valid is None else check_valid
        self.__is_valid__ = self.__check_valid__(self.text)

    def __cheeck_type_valid__(self, text):
        if self.__type__ == int:
            try:
                val = int(text)
                if self.__min__ <= val and val <= self.__max__:
                    self.value = val
                    return True
            except:
                pass
        elif self.__type__ == float:
            try:
                val = float(text)
                if self.__min__ <= val and val <= self.__max__:
                    self.value = val
                    return True
            except:
                pass
        elif self.__type__ == bool:
            try:
                self.value = text.lower() == 'true'
                return True
            except:
                pass
        elif self.__type__ == str:
            self.value = text
            return True
        else:
            raise Exception(f'Type {self.__type__} is not supported.')
        return False

    def __key_input__(self, key):
        super().__key_input__(key)

        if self.__is_focused__:
            # backspace
            if key == 127:
                self.text = self.text[:self.__cursor_pos__-1] + self.text[self.__cursor_pos__:]
                if self.__cursor_pos__ > 0:
                    self.__cursor_pos__ -= 1
                self.__enter_pressed__ = False
            # delete
            elif key == 40:
                self.text = self.text[:self.__cursor_pos__] + self.text[self.__cursor_pos__+1:]
                self.__enter_pressed__ = False
            # arrow left
            elif key == 2:
                self.__cursor_pos__ = self.__cursor_pos__ - 1 if self.__cursor_pos__ > 0 else self.__cursor_pos__
            # arrow right
            elif key == 3:
                self.__cursor_pos__ = self.__cursor_pos__ + 1 if self.__cursor_pos__ < len(self.text) else self.__cursor_pos__
            # enter
            elif key == 13:
                if self.__is_valid__:
                    self.__enter_pressed__ = True
                    self.__is_focused__ = False
            else:
                self.text = self.text[:self.__cursor_pos__] + chr(key) + self.text[self.__cursor_pos__:]
                self.__cursor_pos__ += 1
                self.__enter_pressed__ = False

    def __draw__(self, img):
        super().__draw__(img)
        img = cv.rectangle(img, (self.__px__, self.__py__), (self.__px__ + self.__w__, self.__py__ + self.__h__), color=color.LIGHT_GRAY, thickness=1)
        fh, fw = __get_text_size__(self.text, self.__fontScale__)
        show_cursor = datetime.now() - self.__last_blink_time__ >= self.__cursor_blink_interval__ // 2
        if datetime.now() - self.__last_blink_time__ >= self.__cursor_blink_interval__:
            self.__last_blink_time__ = datetime.now()

        self.__is_valid__ = self.__check_valid__(self.text)
         # invalid border
        if not self.__is_valid__:
            img = cv.rectangle(img, (self.__px__ - self.__margin_outer__, self.__py__ - self.__margin_outer__), (self.__px__ + self.__w__ + self.__margin_outer__, self.__py__ + self.__h__ + self.__margin_outer__), color=color.DARKRED, thickness=1)

        out_text = ''
        for i, c in enumerate(self.text):
            if i == self.__cursor_pos__:
                out_text += self.__cursor__ if show_cursor else ''
                
            out_text += c
        if (self.__cursor_pos__ == len(self.text) or self.__cursor_pos__ == 0) and self.__is_focused__:
            out_text += self.__cursor__ if show_cursor else ' '
        img = cv.putText(img, out_text, (self.__px__, self.__py__ + self.__h__ // 2 + fh // 2), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.4, color=(0, 0, 0))

        return img

class TextBlock(UIElement):
    def __init__(self, label, text, px, py, w = 50, align = 'left', bold = False):
        super().__init__(label, px, py, w, 20, focusable = False)
        self.text = text
        self.__align__ = align
        self.__bold__ = bold

    def __draw__(self, img):
        super().__draw__(img)
        fh, fw = __get_text_size__(self.text, self.__fontScale__)

        thickness = 2 if self.__bold__ else 1

        if self.__align__ == 'center':
            img = cv.putText(img, self.text, (self.__px__ + self.__w__ // 2 - fw // 2, self.__py__ + self.__h__ // 2 + fh // 2),\
                             fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.4, color=(0, 0, 0), thickness=thickness)
        elif self.__align__ == 'left':
            img = cv.putText(img, self.text, (self.__px__, self.__py__ + self.__h__ // 2 + fh // 2),\
                             fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=0.4, color=(0, 0, 0), thickness=thickness)

        return img

class ToggleSwitch(UIElement):
    def __init__(self, label, px, py, on_left_button_clicked = None):
        super().__init__(label, px, py, 40, 20, on_left_button_clicked=on_left_button_clicked)

        self.is_checked = False

    def __mouse_left_button_clicked__(self, x, y):
        if x >= self.__px__ and x <= self.__px__ + self.__w__ and \
            y >= self.__py__ and y <= self.__py__ + self.__h__:
            self.is_checked = not self.is_checked
        super().__mouse_left_button_clicked__(x, y)

    def __draw__(self, img):
        super().__draw__(img)

        # background
        img = cv.rectangle(img, (self.__px__ + self.__h__ // 2, self.__py__ + 4), (self.__px__ + self.__w__ - self.__h__ // 2, self.__py__ + self.__h__ - 4), color=color.LIGHT_GRAY, thickness=-1)
        img = cv.circle(img, (self.__px__ + self.__h__ // 2, self.__py__ + self.__h__ // 2), radius=self.__h__ // 2 - 3, color=color.LIGHT_GRAY, thickness=-1)
        img = cv.circle(img, (self.__px__ + self.__w__ - self.__h__ // 2, self.__py__ + self.__h__ // 2), radius=self.__h__ // 2 - 3, color=color.LIGHT_GRAY, thickness=-1)

        # foreground
        if self.is_checked:
            img = cv.circle(img, (self.__px__ + self.__w__ - self.__h__ // 2, self.__py__ + self.__h__ // 2), radius=self.__h__ // 2, color=color.CORNFLOWER_BLUE, thickness=-1)
        else:
            img = cv.circle(img, (self.__px__ + self.__h__ // 2, self.__py__ + self.__h__ // 2), radius=self.__h__ // 2, color=color.DARK_GRAY, thickness=-1)

        # text
        fh, fw = __get_text_size__(self.label, self.__fontScale__)
        #factor = (fh-1) / self.fontScale
        img = cv.putText(img, self.label, (self.__px__ + self.__w__ + 5, self.__py__ + (self.__h__ - fh) // 2 + fh), cv.FONT_HERSHEY_SIMPLEX, fontScale=self.__fontScale__, color=(0, 0, 0))

        return img
    
class Button(UIElement):
    def __init__(self, label, px, py, w = None, on_left_button_clicked = None):
        super().__init__(label, px, py, 40, 20,\
                         on_left_button_clicked = on_left_button_clicked)

        # text
        fh, fw = __get_text_size__(label, self.__fontScale__)
        self.__fw__ = fw
        self.__fh__ = fh
        self.__w__ = fw + 5 if w is None else w

        self.is_checked = False

    def __mouse_left_button_clicked__(self, x, y):
        super().__mouse_left_button_clicked__(x, y)
        if x >= self.__px__ and x <= self.__px__ + self.__w__ and \
            y >= self.__py__ and y <= self.__py__ + self.__h__:
            self.is_checked = True

    def __mouse_left_button_released__(self, x, y):
        super().__mouse_left_button_released__(x, y)
        if x >= self.__px__ and x <= self.__px__ + self.__w__ and \
            y >= self.__py__ and y <= self.__py__ + self.__h__:
            self.is_checked = False

    def __draw__(self, img):
        super().__draw__(img)

        img = cv.rectangle(img, (self.__px__, self.__py__), (self.__px__ + self.__w__, self.__py__ + self.__h__), color.LIGHT_GRAY, thickness=-1)
        if self.is_checked:
            img = cv.rectangle(img, (self.__px__, self.__py__), (self.__px__ + self.__w__, self.__py__ + self.__h__), color.LIGHT_GRAY, thickness=-1)
        
        img = cv.putText(img, self.label, (self.__px__ + self.__w__ // 2 - self.__fw__ // 2, self.__py__ + (self.__h__ - self.__fh__) // 2 + self.__fh__),\
                         cv.FONT_HERSHEY_SIMPLEX, fontScale=self.__fontScale__, color=color.FOREGROUND if self.__is_enabled__ else color.FOREGROUND_DISABLED)
        return img
    
class Image(UIElement):
    def __init__(self, label, px, py, img, opacity = 1., on_left_button_clicked = None):
        super().__init__(label, px, py, img.shape[1], img.shape[0],\
                         on_left_button_clicked = on_left_button_clicked)

        self.img = img
        self.opacity = opacity

    def __mouse_left_button_clicked__(self, x, y):
        super().__mouse_left_button_clicked__(x, y)

    def __draw__(self, img):
        super().__draw__(img)

        self.__w__ = img.shape[1]
        self.__h__ = img.shape[0]

        #img[self.py:self.py+self.__h__, self.px:self.px+self.__w__] = self.img

        img = drawing.add_overlay(img, self.img, (self.__px__, self.__py__), self.opacity)
        return img
    
class MessageBoxButtons(Enum):
    YES_NO = 1,
    OK_CANCEL = 2,
    OK = 3

class Window():
    def __init__(self, win_name:str, size = (500, 300)):
        self.__win_name__ = win_name
        self.fontScale = 0.4
        self.size = size
        self.__img__ = np.full((size[1], size[0], 3), 255, dtype=np.uint8)
        self.__dispose__ = False
        self.__ui_elements__ = []
        self.confirmed = False

        cv.imshow(self.__win_name__, self.__img__)
        cv.setMouseCallback(self.__win_name__, self.__on_mouse_event__, None)

    def __render__(self):
        self.__img__ = np.full(self.__img__.shape, 255, dtype=np.uint8)
        for ui_element in self.__ui_elements__:
            self.__img__ = ui_element.__draw__(self.__img__)

        cv.imshow(self.__win_name__, self.__img__)
        key = cv.waitKey(10)

        if key != -1:
            for ui_element in self.__ui_elements__:
                ui_element.__key_input__(key)

    def __on_mouse_event__(self, event, x, y, flags, param):
        # mouse left click
        if event == 1:
            for ui_element in self.__ui_elements__:
                ui_element.__mouse_left_button_clicked__(x, y)
        # mouse left button released
        elif event == 4:
            for ui_element in self.__ui_elements__:
                ui_element.__mouse_left_button_released__(x, y)
        # mouse right click
        elif event == 2:
            for ui_element in self.__ui_elements__:
                ui_element.__mouse_right_button_clicked__(x, y)
        # mouse movement
        elif event == 0:
            for ui_element in self.__ui_elements__:
                ui_element.__mouse_moved__(x, y)
        else:
            pass

class OpenFileDialog():
    def __init__(self, dir = None, file_suffix = None, width = 700):
        self.__wind_name__ = 'Open file...'
        self.width = width
        self.__line_height__ = 20
        self.__selected_idx__ = 0

        self.__entries__ = []
        if dir is None:
            for drive in __get_drives_windows__():
                self.__entries__.append(drive)
            for drive in __get_drives_osx__():
                self.__entries__.append(drive)
        else:
            parent_dir = str(Path(dir).parent)
            self.__entries__ = self.__load_entries__(parent_dir)
            for i, d in enumerate(self.__entries__):
                if d == dir:
                    self.__selected_idx__ = i
                    break

        self.__parent_dir__ = self.__entries__[self.__selected_idx__]
        self.__file_suffix__ = file_suffix
        self.confirmed = False
        while not self.confirmed:
            self.__render__()
            cv.waitKey(1)
        cv.destroyWindow(self.__wind_name__)

    def __render__(self):
        self.img = np.ones((10, self.width))
        self.__print_line__('open folder - arrow right')
        self.__print_line__('close folder - arrow left')
        self.__print_line__('next folder - arrow down')
        self.__print_line__('previous folder - arrow up')
        self.__print_line__('select folder - enter')
        self.__print_line__('______________________________________')

        for i, sub_dir in enumerate(self.__entries__):
            is_selected = i == self.__selected_idx__
            self.__print_line__(sub_dir, is_selected)

        cv.imshow(self.__wind_name__, self.img)
        key = cv.waitKey()
        # arrow up
        if key == 0:
            self.__selected_idx__ = self.__selected_idx__ - 1 if self.__selected_idx__ > 0 else self.__selected_idx__
        # arrow down
        elif key == 1:
            self.__selected_idx__ = self.__selected_idx__ + 1 if self.__selected_idx__ < len(self.__entries__) - 1 else self.__selected_idx__
        # arrow right
        elif key == 3:
            if os.path.isdir(self.__entries__[self.__selected_idx__]):
                self.__entries__ = self.__load_entries__(self.__entries__[self.__selected_idx__], self.__file_suffix__)
        # arrow left
        elif key == 2:
            if os.path.isdir(self.__parent_dir__):
                self.__entries__ = self.__load_entries__(self.__parent_dir__, self.__file_suffix__)
        # enter
        elif key == 13:
            if len(self.__entries__) > 0 and os.path.isdir(self.__entries__[self.__selected_idx__]):
                self.path = self.__entries__[self.__selected_idx__]
                self.confirmed = True
        # backspace
        # elif key == 127:
            
        #     pass
        pass

    def __load_entries__(self, dir, file_suffix):
        self.__parent_dir__ = str(Path(dir).parent)
        entries = []
        try:
            for entry in sorted(os.listdir(dir)):
                if os.path.isfile(f'{dir}/{entry}') or file_suffix is not None and entry.endswith(file_suffix):
                        entries.append(f'{dir}/{entry}')
        except:
            pass
        self.__selected_idx__ = 0
        return entries

    def __print_line__(self, text, is_highlighted = False):
        new_line = np.ones((self.__line_height__, self.img.shape[1]))
        if is_highlighted:
            new_line[:, :] = 0.8
        new_line = cv.putText(new_line, text, (10, self.__line_height__//2+3), cv.FONT_HERSHEY_SIMPLEX, 0.4, color=(0, 0, 0), thickness=1)
        self.img = np.concatenate([self.img, new_line])

class OpenFolderDialog():
    def __init__(self, dir = None, width = 700):
        self.__wind_name__ = 'Open folder...'
        self.width = width
        self.__line_height__ = 20
        self.__selected_idx__ = 0

        self.__sub_dirs__ = []
        if dir is None:
            for drive in __get_drives_windows__():
                self.__sub_dirs__.append(drive)
            for drive in __get_drives_osx__():
                self.__sub_dirs__.append(drive)
        else:
            parent_dir = str(Path(dir).parent)
            self.__sub_dirs__ = self.__load_sub_dirs__(parent_dir)
            for i, d in enumerate(self.__sub_dirs__):
                if d == dir:
                    self.__selected_idx__ = i
                    break

        self.__parent_dir__ = self.__sub_dirs__[self.__selected_idx__]
        self.confirmed = False
        while not self.confirmed:
            self.__render__()
            cv.waitKey(1)
        cv.destroyWindow(self.__wind_name__)

    def __render__(self):
        self.img = np.ones((10, self.width))
        self.__print_line__('open folder - arrow right')
        self.__print_line__('close folder - arrow left')
        self.__print_line__('next folder - arrow down')
        self.__print_line__('previous folder - arrow up')
        self.__print_line__('select folder - enter')
        self.__print_line__('______________________________________')

        for i, sub_dir in enumerate(self.__sub_dirs__):
            is_selected = i == self.__selected_idx__
            self.__print_line__(sub_dir, is_selected)

        cv.imshow(self.__wind_name__, self.img)
        key = cv.waitKey()
        # arrow up
        if key == 0:
            self.__selected_idx__ = self.__selected_idx__ - 1 if self.__selected_idx__ > 0 else self.__selected_idx__
        # arrow down
        elif key == 1:
            self.__selected_idx__ = self.__selected_idx__ + 1 if self.__selected_idx__ < len(self.__sub_dirs__) - 1 else self.__selected_idx__
        # arrow right
        elif key == 3:
            self.__sub_dirs__ = self.__load_sub_dirs__(self.__sub_dirs__[self.__selected_idx__])
        # arrow left
        elif key == 2:
            self.__sub_dirs__ = self.__load_sub_dirs__(self.__parent_dir__)
        # enter
        elif key == 13:
            if len(self.__sub_dirs__) > 0 and os.path.isdir(self.__sub_dirs__[self.__selected_idx__]):
                self.path = self.__sub_dirs__[self.__selected_idx__]
                self.confirmed = True
        # backspace
        # elif key == 127:
            
        #     pass
        pass

    def __load_sub_dirs__(self, dir):
        self.__parent_dir__ = str(Path(dir).parent)
        sub_dirs = []
        try:
            for entry in sorted(os.listdir(dir)):
                if os.path.isdir(f'{dir}/{entry}'):
                    sub_dirs.append(f'{dir}/{entry}')
        except:
            pass
        self.__selected_idx__ = 0
        return sub_dirs

    def __print_line__(self, text, is_highlighted = False):
        new_line = np.ones((self.__line_height__, self.img.shape[1]))
        if is_highlighted:
            new_line[:, :] = 0.8
        new_line = cv.putText(new_line, text, (10, self.__line_height__//2+3), cv.FONT_HERSHEY_SIMPLEX, 0.4, color=(0, 0, 0), thickness=1)
        self.img = np.concatenate([self.img, new_line])

class TextInputDialog(Window):
    def __init__(self, win_name, text = '', check_valid = None):
        super().__init__(win_name, size=(500, 80))

        self.__txt_header__ = TextBlock(None, self.__win_name__, px=5, py=5)
        self.__txt_input__ = TextBox(None, text, px=5, py=30, w=self.size[0]-10, check_valid=check_valid)
        self.__txt_input__.__is_focused__ = True
        self.__btn_cancel__ = Button('Cancel', px=5, py = 55, w = self.size[0]//2-10, on_left_button_clicked=self.__on_btn_cancel_clicked__)
        self.__btn_save__ = Button('Save', px=self.size[0]//2+5, py = 55, w = self.size[0]//2-10, on_left_button_clicked=self.__on_btn_save_clicked__)
        self.text = text

        self.__ui_elements__ = [
            self.__txt_header__,
            self.__txt_input__,
            self.__btn_cancel__,
            self.__btn_save__
        ]

        self.confirmed = False
        
        while not self.confirmed:
            self.__render__()
            key = cv.waitKey(1)
            self.__key_input__(key)
            if self.__btn_cancel__.is_checked:
                cv.destroyWindow(self.__win_name__)
                break
            if self.__txt_input__.__enter_pressed__ or self.__btn_save__.is_checked:
                self.text = self.__txt_input__.text
                self.confirmed = True
        cv.destroyWindow(self.__win_name__)

    def __on_btn_cancel_clicked__(self):
        cv.destroyWindow(self.__win_name__)

    def __on_btn_save_clicked__(self):
        self.text = self.__txt_input__.text
        self.confirmed = True
        cv.destroyWindow(self.__win_name__)

    def __render__(self):
        super().__render__()

    def __key_input__(self, key):
        if key == -1:
            return
        for ui_element in self.__ui_elements__:
            ui_element.__key_input__(key)

class MessageBox(Window):
    def __init__(self, caption:str, message:str, buttons:MessageBoxButtons):
        super().__init__(caption)
        fh, fw = __get_text_size__(message, self.fontScale)
        self.__size__ = (fw + 10, fh + 10 + 40)
        self.__img__ = np.ones((self.__size__[1], self.__size__[0], 3), dtype=np.float32)

        self.__ui_elements__ = [
            TextBlock(None, message, px=5, py=5, align='left', bold=False)
        ]

        if buttons == MessageBoxButtons.YES_NO:
            self.__ui_elements__.append(Button('Yes', px=5, py=5+fh+20, w=self.__size__[0]//2-10, on_left_button_clicked=self.on_accept))
            self.__ui_elements__.append(Button('No', px=self.__size__[0]//2 + 5, py=5+fh+20, w=self.__size__[0]//2-10, on_left_button_clicked=self.on_decline))
        elif buttons == MessageBoxButtons.OK_CANCEL:
            self.__ui_elements__.append(Button('Ok', px=5, py=5+fh+20, w=self.__size__[0]//2-10, on_left_button_clicked=self.on_accept))
            self.__ui_elements__.append(Button('Cancel', px=self.__size__[0]//2 + 5, py=5+fh+20, w=self.__size__[0]//2-10, on_left_button_clicked=self.on_decline))
        elif buttons == MessageBoxButtons.OK:
            self.__ui_elements__.append(Button('Ok', px=5, py=5+fh+20, w=self.__size__[0]-10, on_left_button_clicked=self.on_accept))

        self.__render__()

        self.confirmed = None

        while self.confirmed is None:
            cv.waitKey(1)
        cv.destroyWindow(self.__win_name__)

    def on_decline(self):
        self.confirmed = False

    def on_accept(self):
        self.confirmed = True
        
if __name__ == '__main__':
    ofd = OpenFileDialog(file_suffix='.pt')

    class TestWindow(Window):
        def __init__(self):
            super().__init__('Test Window')

            img = np.full((100, 100, 3), 255, dtype=np.uint8)
            img = cv.circle(img, (50, 50), radius=40, color=(0, 0, 255), thickness=-1)

            self.__ui_elements__.append(Image('', 0, 0, img))
            self.__render__()

    testWindow = TestWindow()

    dialog = TextInputDialog('TextInputDialog')
    dialog = OpenFolderDialog()
    dialog = MessageBox('MessageBox', 'Message', MessageBoxButtons.YES_NO)