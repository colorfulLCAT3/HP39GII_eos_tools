import os
import subprocess

# 设置 ffmpeg 路径
ffmpeg_path = r'I:\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe'

# 输出配置
TARGET_WIDTH = 255
TARGET_FPS = 24
OUTPUT_SUFFIX = '_mjpeg.avi'
SUPPORTED_INPUT_EXTS = ['.mp4', '.avi', '.mov', '.mkv', '.flv']


def prompt_time_range(filename):
    print(f"\n🟡 正在处理: {filename}")
    while True:
        try:
            start = float(input("请输入起始时间（单位：秒，例如 0）："))
            end = float(input("请输入结束时间（单位：秒，例如 10）："))
            if end <= start:
                print("⚠️ 结束时间必须大于起始时间，请重新输入。")
                continue
            return start, end
        except ValueError:
            print("⚠️ 输入无效，请输入数字。")


def convert_to_mjpeg(input_path, output_path, start_time, duration):
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)

    # 缩放宽度为255，按比例适配高度
    vf_filter = f"scale={TARGET_WIDTH}:-2"

    ffmpeg_cmd = [
        ffmpeg_path,
        '-y',
        '-ss', str(start_time),
        '-i', input_path,
        '-t', str(duration),
        '-vf', vf_filter,
        '-r', str(TARGET_FPS),                # 👈 设置输出帧率为 24fps
        '-vcodec', 'mjpeg',
        '-q:v', '5',
        '-pix_fmt', 'yuvj420p',
        '-an',
        '-f', 'avi',
        output_path
    ]

    print("▶️ 正在转换：", input_path)
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f'✅ 转换成功: {output_path}\n')
    except subprocess.CalledProcessError as e:
        print(f'❌ 转换失败: {input_path}\n   错误: {e}\n')


def convert_all_videos_in_folder(folder='.'):
    for filename in os.listdir(folder):
        name, ext = os.path.splitext(filename)
        ext = ext.lower()

        if ext in SUPPORTED_INPUT_EXTS and not filename.endswith(OUTPUT_SUFFIX):
            input_path = os.path.join(folder, filename)
            output_path = os.path.join(folder, name + OUTPUT_SUFFIX)
            start_time, end_time = prompt_time_range(filename)
            duration = end_time - start_time
            convert_to_mjpeg(input_path, output_path, start_time, duration)


if __name__ == '__main__':
    convert_all_videos_in_folder()
