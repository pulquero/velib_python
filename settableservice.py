from settingsdevice import SettingsDevice


class SettableService:
    def __init__(self):
        self.supportedSettings = {}
        self.settablePaths = {}

    def _init_settings(self, conn):
        self.settings = SettingsDevice(conn, self.supportedSettings, self._setting_changed)
        self.initializingSettings = True
        for settingName in self.supportedSettings.keys():
            path = self.settablePaths[settingName]
            self.service[path] = self.settings[settingName]
        self.initializingSettings = False

    def _get_settings_path(self, subPath):
        return f"/Settings/{self.service.serviceType.capitalize()}/{self.service.serviceAddress}{subPath}"

    def add_settable_path(self, subPath, initialValue, minValue=0, maxValue=0, **kwargs):
        settingName = subPath[1:].lower()
        self.service.add_path(subPath, initialValue, writeable=True, onchangecallback=lambda path, newValue: self._value_changed(settingName, newValue), **kwargs)
        self.supportedSettings[settingName] = [
            self._get_settings_path(subPath),
            initialValue,
            minValue,
            maxValue
        ]
        self.settablePaths[settingName] = subPath

    def _value_changed(self, settingName, newValue):
        # ignore events generated during initialization
        if not self.initializingSettings:
            # this should trigger a _setting_changed() call
            self.settings[settingName] = newValue

    def _setting_changed(self, settingName, oldValue, newValue):
        path = self.settablePaths[settingName]
        self.service[path] = newValue
