# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'it-boy'
copyright = '2024, zys'
author = 'zys'
release = 'v0.1'
version = "v0.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
# 添加对markdown的支持,markdown的表格语法支持
extensions = ['recommonmark', 'sphinx_markdown_tables']

# 这个需要自己加上，这里主要说明什么格式的文件由什么解析
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

# 模板的存放路径， 自定义主题时使用
templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
# html主题的相关设置
html_theme_options = {"collapse_navigation": False, "navigation_depth": 6}
# 在页面底部显示上一次更新于某某时间
html_last_updated_fmt = "%Y-%m-%d %H:%M:%S"
# 根文档的rst文件的文档名称，其实就是source下面的index.rst文件的名称，可以自定义
root_doc = "index"
# 代码高亮的风格, 如未设置，则使用默认样式或者使用sphinx指定的html样式
pygments_style = 'sphinx'
# 是否显示版本，对于read the doc来说就是左上角的版本号
display_version = True
# 是否显示查看源码链接
html_show_sourcelink = False
