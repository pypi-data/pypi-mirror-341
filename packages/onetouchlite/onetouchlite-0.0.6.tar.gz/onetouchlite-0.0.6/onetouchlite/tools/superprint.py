"""
蓝色：通常与信任、稳定性和专业性相关联。如果模型的信息需要传达一种可靠和权威的感觉，蓝色是一个不错的选择。                              信息
绿色：与积极、成长和成功相关。如果模型的信息是正面的，如高准确率或成功的预测，绿色可以用来强调这一点。                                 结果
红色：通常与警告、危险或错误相关。如果模型的信息中包含重要的警告或需要注意的问题，如高错误率或潜在的风险，使用红色可以突出这些问题。         错误
黄色：用于吸引注意，通常与警告或提示相关，但没有红色那么强烈。如果需要引起对某些信息的注意，但又不至于显得过于严重，黄色可以是一个选项。      警告
灰色：通常用于中性信息或作为背景色。如果模型的信息不需要特别强调，或者你想要创造一种中性和专业的氛围，灰色是合适的选择。                   背景
青色: OneTouch本身想要告诉使用者的信息                                                                                OneTouch
"""

colors = {
    'default': '\033[0m',  # 默认颜色
    'black': '\033[30m',  # 黑色文本
    'red': '\033[31m',  # 红色文本
    'green': '\033[32m',  # 绿色文本
    'yellow': '\033[33m',  # 黄色文本
    'blue': '\033[34m',  # 蓝色文本
    'magenta': '\033[35m',  # 品红色文本
    'cyan': '\033[36m',  # 青色文本
    'white': '\033[37m',  # 白色文本
    'bright_black': '\033[90m',  # 灰色（变亮的黑色文本）
    'bright_red': '\033[91m',  # 亮红色文本
    'bright_green': '\033[92m',  # 亮绿色文本
    'bright_yellow': '\033[93m',  # 亮黄色文本
    'bright_blue': '\033[94m',  # 亮蓝色文本
    'bright_magenta': '\033[95m',  # 亮品红色文本
    'bright_cyan': '\033[96m',  # 亮青色文本
    'bright_white': '\033[97m'  # 亮白色文本
}


class Style:
    def __init__(self, style=None, morphology=None):
        self.style = style
        self.morphology = morphology
        self.list_style = []

        self.__convert_morphology(self.morphology)
        self.__convert_style()

        self.font = self.__connect_style()

    class Color:
        black = '\033[30m'  # 黑色文本
        red = '\033[31m'  # 红色文本
        green = '\033[32m'  # 绿色文本
        yellow = '\033[33m'  # 黄色文本
        blue = '\033[34m'  # 蓝色文本
        magenta = '\033[35m'  # 品红色文本
        cyan = '\033[36m'  # 青色文本
        white = '\033[37m'  # 白色文本
        bright_black = '\033[90m'  # 灰色（变亮的黑色文本）
        bright_red = '\033[91m'  # 亮红色文本
        bright_green = '\033[92m'  # 亮绿色文本
        bright_yellow = '\033[93m'  # 亮黄色文本
        bright_blue = '\033[94m'  # 亮蓝色文本
        bright_magenta = '\033[95m'  # 亮品红色文本
        bright_cyan = '\033[96m'  # 亮青色文本
        bright_white = '\033[97m'  # 亮白色文本

    class BackgroundColor:
        black = '\033[40m'  # 黑色背景
        red = '\033[41m'  # 红色背景
        green = '\033[42m'  # 绿色背景
        yellow = '\033[43m'  # 黄色背景
        blue = '\033[44m'  # 蓝色背景
        magenta = '\033[45m'  # 品红色背景
        cyan = '\033[46m'  # 青色背景
        white = '\033[47m'  # 白色背景
        bright_black = '\033[100m'  # 灰色背景（变亮的黑色）
        bright_red = '\033[101m'  # 亮红色背景
        bright_green = '\033[102m'  # 亮绿色背景
        bright_yellow = '\033[103m'  # 亮黄色背景
        bright_blue = '\033[104m'  # 亮蓝色背景
        bright_magenta = '\033[105m'  # 亮品红色背景
        bright_cyan = '\033[106m'  # 亮青色背景
        bright_white = '\033[107m'  # 亮白色背景

    def __convert_style(self):
        if self.style is not None:
            attributes = self.style.split(';')[:-1]  # Removing the last empty string after the last semicolon
            attributes = {attr.split(':')[0].strip(): attr.split(':')[1].strip() for attr in attributes}
            self.__convert_morphology(attributes)

    def __convert_morphology(self, morphology):
        if morphology is not None:
            for key, value in morphology.items():
                if key == 'color':
                    self.list_style.append(getattr(Style.Color, value))
                elif key == 'backgroundcolor':
                    self.list_style.append(getattr(Style.BackgroundColor, value))
                elif key == 'bold':
                    if value:
                        self.list_style.append('\033[1m')
                    else:
                        self.list_style.append('\033[22m')
                elif key == 'faint':
                    if value:
                        self.list_style.append('\033[2m')
                    else:
                        self.list_style.append('\033[1m')
                elif key == 'italic':
                    if value:
                        self.list_style.append('\033[3m')
                    else:
                        self.list_style.append('\033[23m')
                elif key == 'underline':
                    if value:
                        self.list_style.append('\033[4m')
                    else:
                        self.list_style.append('\033[24m')
                elif key == 'reverse':
                    if value:
                        self.list_style.append('\033[7m')
                    else:
                        self.list_style.append('\033[27m')
                elif key == 'crossed-out':
                    if value:
                        self.list_style.append('\033[9m')
                    else:
                        self.list_style.append('\033[29m')

    def __connect_style(self):
        if self.list_style:
            list_style = ''.join(self.list_style)
            return list_style
        else:
            return ''


def prints(self, *args, display: bool = True, style: str = None, morphology: dict = None, recover: bool = True, sep='',
           end='\n', file=None):
    styles = Style(style, morphology)

    if recover:
        recovers = '\033[0m'
    else:
        recovers = ''

    if display:
        print(f'{styles.font}', self, *args, recovers, sep=sep, end=end, file=file)


def printc(self, *args, display: bool = True, color: str = None, sep: str = ' ', end: str = '\n', file=None) -> None:
    """
        Prints the values to a stream, or to sys.stdout by default.

          sep
            string inserted between values, default a space.
          end
            string appended after the last value, default a newline.
          file
            a file-like object (stream); defaults to the current sys.stdout.
          flush
            whether to forcibly flush the stream.
    """
    color = colors.get(color, colors['default'])

    if display:
        print(f'{color}{self}', *args, '\033[0m', sep=sep, end=end, file=file)
