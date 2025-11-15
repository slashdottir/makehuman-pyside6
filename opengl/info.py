"""
    License information: data/licenses/makehuman_license.txt
    Author: black-punkduck

    Functions:
    * openGLError

    Classes:
    * GLDebug
"""

import OpenGL
from OpenGL import GL as gl


def openGLError():
    while True:
        a = gl.glGetError()
        if a == gl.GL_NO_ERROR:
            return
        print(a)


class GLDebug:
    def __init__(self, initialized=True):
        self.initialized = initialized
        self.min_version = (2,1) # (3, 3)

    def getOpenGL_LibVers(self):
        return OpenGL.__version__

    def minVersion(self):
        return str(self.min_version)

    def _as_int(self, value):
        # PyOpenGL may return an array-like or a single int
        try:
            if hasattr(value, '__len__') and not isinstance(value, (str, bytes)):
                return int(value[0])
            return int(value)
        except Exception:
            return 0

    def getVersion(self):
        if not self.initialized:
            return (0, 0)

        try:
            # Preferred: read MAJOR/MINOR via glGetIntegerv
            maj = self._as_int(gl.glGetIntegerv(gl.GL_MAJOR_VERSION))
            minv = self._as_int(gl.glGetIntegerv(gl.GL_MINOR_VERSION))
            if maj == 0 and minv == 0:
                # fallback: parse GL_VERSION string
                maj, minv = self._parse_version_string()
            return (maj, minv)
        except Exception:
            # If anything goes wrong (no context, unsupported enums), try fallback parse
            maj, minv = self._parse_version_string()
            return (maj, minv)

    def _parse_version_string(self):
        """Parse version from GL_VERSION string like '2.1 Metal - 90.5' or '4.1'"""
        try:
            ver = gl.glGetString(gl.GL_VERSION)
            if ver:
                # Handle both bytes and str
                if isinstance(ver, bytes):
                    ver = ver.decode('utf-8')
                # Extract first token (e.g. '2.1' from '2.1 Metal - 90.5')
                version_str = ver.split()[0]
                parts = version_str.split('.')
                maj = int(parts[0]) if len(parts) > 0 else 0
                minv = int(parts[1]) if len(parts) > 1 else 0
                return (maj, minv)
        except Exception:
            pass
        return (0, 0)

    def checkVersion(self):
        major, minor = self.getVersion()
        return ((major, minor) >= self.min_version)

    def getExtensions(self):
        extensions = []
        if not self.initialized:
            return extensions

        try:
            n = self._as_int(gl.glGetIntegerv(gl.GL_NUM_EXTENSIONS))
            for i in range(0, n):
                s = gl.glGetStringi(gl.GL_EXTENSIONS, i)
                if s:
                    extensions.append(s.decode('utf-8'))
        except Exception:
            # older drivers: try glGetString(GL_EXTENSIONS) which returns a space-separated list
            try:
                all_ext = gl.glGetString(gl.GL_EXTENSIONS)
                if all_ext:
                    extensions = all_ext.decode('utf-8').split()
            except Exception:
                pass

        return extensions

    def getShadingLanguages(self):
        languages = []
        if not self.initialized:
            return languages

        try:
            n = self._as_int(gl.glGetIntegerv(gl.GL_NUM_SHADING_LANGUAGE_VERSIONS))
            for i in range(0, n):
                s = gl.glGetStringi(gl.GL_SHADING_LANGUAGE_VERSION, i)
                if s:
                    languages.append(s.decode('utf-8'))
        except Exception:
            # fallback: single shading language string
            try:
                s = gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)
                if s:
                    languages.append(s.decode('utf-8'))
            except Exception:
                pass

        return languages

    def getCard(self):
        try:
            s = gl.glGetString(gl.GL_VERSION)
            return s.decode('utf-8') if s else 'unknown'
        except Exception:
            return 'not initialized'

    def getRenderer(self):
        try:
            s = gl.glGetString(gl.GL_RENDERER)
            return s.decode('utf-8') if s else 'unknown'
        except Exception:
            return 'not initialized'

    def getInfo(self):
        info = {}
        info['min_version'] = self.minVersion()
        info['version'] = self.getVersion()
        info['card'] = self.getCard()
        info['renderer'] = self.getRenderer()
        info['languages'] = self.getShadingLanguages()
        info['extensions'] = self.getExtensions()
        return info

    def getTextInfo(self):
        text = 'Minimum version demanded: ' + str(self.min_version) + \
            '<br>Highest version available: ' + str(self.getVersion()) + \
            '<br>Card Driver: ' + self.getCard() + \
            '<br>Renderer: ' + self.getRenderer() + \
            '<p>Shading languages:'

        lang = self.getShadingLanguages()
        for l in lang:
            text += '<br>' + l

        text += '<p>Extensions:'
        ext = self.getExtensions()
        for l in ext:
            text += '<br>' + l

        return text
