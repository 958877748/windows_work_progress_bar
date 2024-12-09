# Windows Work Progress Bar

## 功能
- 在屏幕最上方显示一个几像素高的进度条
- 标明今天的上下班时间和进度
- 使用Python开发
- 不要影响下方界面的交互
- 已完成进度部分显示绿色
- 未完成部分显示灰色
- 高度为2像素
- 始终显示在其他UI上方

## 配置
使用 `config.yaml` 文件自定义工作时间和进度条外观：

```yaml
work_hours:
  start_time: "09:30"  # 工作开始时间
  end_time: "18:30"    # 工作结束时间

progress_bar:
  height: 2            # 进度条高度（像素）
  completed_color: "green"     # 已完成部分颜色
  uncompleted_color: "gray"    # 未完成部分颜色

breaks:
  - start: "12:00"     # 午休开始时间
    end: "13:00"       # 午休结束时间
    exclude_from_progress: true  # 是否从进度计算中排除
```

## 安装依赖
```bash
pip install -r requirements.txt
```

## 运行
```bash
python progress_bar.py