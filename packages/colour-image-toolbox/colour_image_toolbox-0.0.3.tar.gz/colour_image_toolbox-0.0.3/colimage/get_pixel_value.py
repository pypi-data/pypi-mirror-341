import rawpy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
import os

file_path = r"C:\Users\Jackc\Desktop\Canon600D_0001.CR2"

# file_path = r"C:\Users\Jackc\Desktop\DSC05717.ARW"

def readrawfile(filename) -> np.ndarray:
    with rawpy.imread(filename) as raw:
        raw_img = raw.postprocess(
            gamma=(1, 1),
            output_bps=16,
            user_wb=[1, 1, 1, 1],
            output_color=rawpy.ColorSpace.raw,
            no_auto_bright=True,
            # half_size=True, # half size
        )
    raw_img = np.clip(raw_img / 65535, 0, 1).astype(np.float64)
    return raw_img

def display_raw_image(img_array):
    """显示RAW图像并设置鼠标点击事件"""
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(img_array)
    ax.set_title('RAW Image - Click to get pixel values')
    
    # 创建输出文件
    output_dir = os.path.dirname(file_path)
    output_file = os.path.join(output_dir, "pixel_values.txt")
    
    # 初始化输出文件，写入标题行
    with open(output_file, 'w') as f:
        f.write("X\tY\tR\tG\tB\tR/G\tB/G\n")
    
    # 存储r/g和b/g比值用于绘制散点图
    r_g_ratios = []
    b_g_ratios = []
    
    def on_click(event: MouseEvent):
        if event.xdata is not None and event.ydata is not None:
            x, y = int(event.xdata), int(event.ydata)
            
            # 确保坐标在图像范围内
            if 0 <= x < img_array.shape[1] and 0 <= y < img_array.shape[0]:
                pixel_value = img_array[y, x]
                
                # 对于RGB图像
                if len(pixel_value) == 3:
                    r, g, b = pixel_value
                    r_g_ratio = r / g if g > 0 else float('inf')
                    b_g_ratio = b / g if g > 0 else float('inf')
                    
                    # 存储比值用于散点图
                    if r_g_ratio != float('inf') and b_g_ratio != float('inf'):
                        r_g_ratios.append(r_g_ratio)
                        b_g_ratios.append(b_g_ratio)
                    
                    # 显示在控制台
                    print(f"Position: ({x}, {y})")
                    print(f"R: {r:.6f}, G: {g:.6f}, B: {b:.6f}")
                    print(f"R/G: {r_g_ratio:.6f}, B/G: {b_g_ratio:.6f}")
                    
                    # 保存到文件
                    with open(output_file, 'a') as f:
                        f.write(f"{x}\t{y}\t{r:.6f}\t{g:.6f}\t{b:.6f}\t{r_g_ratio:.6f}\t{b_g_ratio:.6f}\n")
                    
                    # 更新标题显示当前像素值
                    ax.set_title(f"Position: ({x}, {y}) - R: {r:.4f}, G: {g:.4f}, B: {b:.4f}, R/G: {r_g_ratio:.4f}, B/G: {b_g_ratio:.4f}")
                    fig.canvas.draw_idle()
    
    # 连接鼠标点击事件
    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.tight_layout()
    plt.show()
    
    # 在用户关闭图像窗口后，生成散点图
    if r_g_ratios and b_g_ratios:
        create_ratio_scatter_plot(r_g_ratios, b_g_ratios, output_dir)

def create_ratio_scatter_plot(r_g_ratios, b_g_ratios, output_dir):
    """创建R/G和B/G比值的散点图并保存为SVG"""
    plt.figure(figsize=(10, 8))
    plt.scatter(r_g_ratios, b_g_ratios, color='blue', alpha=0.7, edgecolors='k', s=80)
    plt.xlabel('R/G Ratio')
    plt.ylabel('B/G Ratio')
    plt.title('R/G vs B/G Ratio Distribution')
    # Set axis limits from 0 to 1
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 添加比例线
    if r_g_ratios and b_g_ratios:
        max_r_g = max(r_g_ratios)
        max_b_g = max(b_g_ratios)
        max_val = max(max_r_g, max_b_g) * 1.1
        plt.plot([0, max_val], [0, max_val], 'r--', alpha=0.5, label='1:1 Line')
    
    plt.tight_layout()
    plt.legend()
    
    # 保存为SVG
    output_path = os.path.join(output_dir, "ratio_scatter_plot.svg")
    plt.savefig(output_path, format='svg')
    print(f"Scatter plot saved to: {output_path}")
    
    # 显示散点图
    plt.show()

def main():
    """主函数：读取RAW文件并显示"""
    try:
        raw_img = readrawfile(file_path)
        print(f"shape: {raw_img.shape}, dtype: {raw_img.dtype}")
        print(f"Image shape: {raw_img.shape}, dtype: {raw_img.dtype}")

        display_raw_image(raw_img)
        # display_raw_image(raw_img)
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    main()


