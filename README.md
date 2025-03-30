# 结构目录

桌宠项目/
├── assets/                    # 存放资源文件（例如宠物图像、声音等）
│   ├── icon.py                # icon
│   ├── pet_a/                 # 桌宠A的所有资源
│   │   ├── idle/              # 宠物A的闲置动作图像
│   │   │   ├── idle_1.png    # 闲置动作1
│   │   │   ├── idle_2.png    # 闲置动作2
│   │   ├── walking/           # 宠物A的行走动作图像
│   │   │   ├── walk_1.png    # 行走动作1
│   │   │   ├── walk_2.png    # 行走动作2
│   │   ├── a_a/               # 宠物A的特殊动作（A-A互动）
│   │   │   ├── a_a_1.png     # A-A互动动作1
│   │   │   ├── a_a_2.png     # A-A互动动作2
│   │   ├── a_b/               # 宠物A的特殊动作（A-B互动）
│   │   │   ├── a_b_1.png     # A-B互动动作1
│   │   │   ├── a_b_2.png     # A-B互动动作2
│   │   ├── sound/             # 宠物A的音效
│   │   └── animation/         # 宠物A的动画资源（例如背景动画）
│   └── pet_b/                 # 桌宠B的所有资源
│       ├── idle/              # 宠物B的闲置动作图像
│       ├── walking/           # 宠物B的行走动作图像
│       ├── b_a/               # 宠物B的特殊动作（B-A互动）
│       │   ├── b_a_1.png     # B-A互动动作1
│       │   ├── b_a_2.png     # B-A互动动作2
│       ├── sound/             # 宠物B的音效
│       └── animation/         # 宠物B的动画资源
├── pets/                      # 桌宠类和功能的定义
│   ├── pet_manager.py          #管理全局的宠物 
│   ├── tray_menu.py            # 菜单栏，应包含退出、召唤、允许互动范围
│   ├── base_pet.py            # 桌宠基类：提供行走、重力、拖拽、闲置功能
│   ├── interactive_pet.py     # 交互功能（如互动窗口、宠物间互动）
│   ├── animated_pet.py        # 动画功能（管理动作、切换动画、基于图片底部对齐）
│   ├── pet_a.py               # 桌宠A的实现（支持A-A和A-B互动）
│   └── pet_b.py               # 桌宠B的实现（支持B-A互动）
├── utils/                     # 工具类
│   ├── upper.py               # 上界计算，应优化为窗口输出
├── main.py                    # 启动程序，初始化桌宠并管理
├── requirements.txt           # 依赖库（如PyQt5、requests等）
├── README.md                  # 项目说明文档
└── setup.py                   # 安装和打包配置


# prompt

我希望它是一个最终可以封装并部署到其他人电脑上的桌宠，具备基础的功能比如显示拖动动画和与桌面上的窗口和其他桌宠互动，并且可以在桌面产生多个不同的桌宠，比如桌宠a，桌宠b，他们底层功能相同，但可能具备一些不同的功能，比如桌宠a有互动a，b没有。另外还有表单提供可选的功能，比如是否启用ai，给我一步一步的实现逻辑和文件架构

按照这个目录结构分文件给我对应的代码，桌宠的都具有，自由行走，闲置、自由拖拽功能与对应动画。之后可能会有a具有特殊动作a1，a2，b具有特殊动作b1,b2，这个之后再写


基类功能-闲逛（向左、向右）、重力、静止、拖拽、爬行
特殊功能-桌宠互动、自定义闲置状态
菜单-自定义招出桌宠等生成

打包程序与部署

优化惯性参数、针对窗口互动


直接在菜单上增加，允许互动窗口，一旦允许，那么窗口的上界将允许站立行为、攀爬行为

菜单需要-召唤宠物-随机一只、确定的某一只；窗口互动允许-具体哪些窗口可选；ai接口配置
消灭一只宠物

优化upper更名为窗口选择，提供允许互动的窗口
一旦允许后，灰狗将把它作为可互动的（可站立、攀爬）