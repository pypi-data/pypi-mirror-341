import xmltodict
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QScrollArea, QBoxLayout, QFormLayout, QGraphicsAnchorLayout,QGraphicsGridLayout,QGraphicsLayout,QGraphicsLinearLayout,QGridLayout,QHBoxLayout,QLayout,QPlainTextDocumentLayout,QStackedLayout,QVBoxLayout
from app_page.utils import setWidgetStyle
from app_page.utils.common import unescape_xml

renameWidgetMap = {
  'widget': 'QWidget',
  'grid': 'QGridLayout',
  'h-box': 'QHBoxLayout',
  'v-box': 'QVBoxLayout',
  'label': 'QLabel',
  'button': 'QPushButton',
  'line-edit': 'QLineEdit',
  'text-edit': 'QPlainTextEdit',
  'selector': 'QComboBox',
}

def scrollLayout(layout:QLayout, style:str="background-color: transparent;"):
  scroll_area = QScrollArea()
  scroll_area.setWidgetResizable(True)
  scroll_area.setStyleSheet(style)
  content_widget = QWidget()
  scroll_area.setWidget(content_widget)
  content_layout = QVBoxLayout(content_widget)
  content_layout.setContentsMargins(0, 0, 0, 0)
  layout.addWidget(scroll_area)
  return content_layout

def render(layout, template:str):
  """渲染模板

  参数:
      layout (object): 父布局
      template (str): 模板字符串

  返回:
      widgetIdMap(dict): 组件id与组件的映射关系
  """
  widgetIdMap = {}
  components, scroll = template_to_components(template)
  if scroll:
    layout = scrollLayout(layout)
  inner_render(layout, components, widgetIdMap)
  return widgetIdMap

def checkLayout(value):
  return isinstance(value, QGridLayout) or isinstance(value, QHBoxLayout) or isinstance(value, QVBoxLayout)

def inner_render(layout:QWidget|QBoxLayout|QFormLayout|QGraphicsAnchorLayout|QGraphicsGridLayout|QGraphicsLayout|QGraphicsLinearLayout|QGridLayout|QHBoxLayout|QLayout|QPlainTextDocumentLayout|QStackedLayout|QVBoxLayout, components:list, widgetIdMap:dict):
  for component in components:
    if isinstance(component, dict) and 'type' in component:
      WidgetType = getattr(QtWidgets, component['type']) if hasattr(QtWidgets, component['type']) else None
      if WidgetType and checkLayout(layout):
        widget:QWidget = WidgetType()
        if 'grid' in component:
          grid = component['grid']
          layout.addWidget(widget, *grid)
        else:
          layout.addWidget(widget)
      else:
        widget:QWidget|QGridLayout|QHBoxLayout|QVBoxLayout = WidgetType(layout)

      keys = component.keys()
      for key in keys:
        value = component[key]
        if key == 'id':
          widget.setObjectName(value)
          widgetIdMap[value] = widget
        elif key == 'text':
          if isinstance(widget, QtWidgets.QPlainTextEdit):
            widget.setPlainText(unescape_xml(value))
            return
          widget.setText(unescape_xml(value))
        elif key == 'title':
          if hasattr(widget, 'setToolTip'):
            widget.setToolTip(unescape_xml(value))
        elif key == 'style':
          if isinstance(value, str):
            widget.setStyleSheet(value)
          elif callable(value):
            value(widget)
          else:
            setWidgetStyle(widget, value, cover=True)
        elif key == 'margins':
          widget.setContentsMargins(*value)
        elif key == 'spacing':
          widget.setSpacing(value)
        elif key == 'width':
          widget.setFixedWidth(value)
        elif key == 'height':
          widget.setFixedHeight(value)
        elif key == 'disabled':
          if hasattr(widget, 'setReadOnly'):
            widget.setReadOnly(value != 'False')
        elif key == 'placeholder':
          if hasattr(widget, 'setPlaceholderText'):
            widget.setPlaceholderText(unescape_xml(value))
        elif key == 'password':
          if hasattr(widget, 'setEchoMode'):
            widget.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        elif key == 'align':
          if hasattr(widget, 'setAlignment') and hasattr(Qt, value):
            widget.setAlignment(getattr(Qt, value))
        elif key == 'scroll':
          if isinstance(widget, QLayout) and value == 'True':
            widget.__content_layout = scrollLayout(widget, value)
        elif key == 'children':
          if hasattr(widget, '__content_layout'):
            widget_or_layout = widget.__content_layout
            delattr(widget, '__content_layout')
          else:
            widget_or_layout = widget
          inner_render(widget_or_layout, value if isinstance(value, list) else [value], widgetIdMap)

def template_to_components(template:str) -> tuple:
  """将xml模板转换为组件列表。

  参数:
      template (str): xml模板

  返回:
      components(list): 组件列表
  """
  # 将xml字符串转换为字典
  xml_dict = xmltodict.parse(template)

  def process_element(element):
    if not isinstance(element, dict):
      return {}

    component = {}
    for key in element.keys():
      if key.startswith('@'):
        if key == '@margins' or key == '@grid':
          component[key[1:]] = list(map(int, element[key].strip("[]").split(',')))
        elif key in ['@spacing', '@width', '@height']:
          component[key[1:]] = int(element[key])
        else:
          component[key[1:]] = element[key]
      
      elif key == 'layout':
        layout = element['layout']
        children = []
        if isinstance(layout, dict):
          dataList = []
          item = {}
          # 获取layout中开头不是@的属性的键值对
          for _key in layout.keys():
            if _key.startswith('@'):
              if _key == '@margins' or _key == '@grid':
                item[_key[1:]] = list(map(int, layout[_key].strip("[]").split(',')))
              elif _key in ['@spacing', '@width', '@height']:
                item[_key[1:]] = int(layout[_key])
              else:
                item[_key[1:]] = layout.get(_key, '')
              continue
            child = layout.get(_key, None)
            if isinstance(child, dict):
              typeValue = renameWidgetMap[_key] if _key in renameWidgetMap else _key
              dataList.append({**child, '@type': typeValue})
            elif isinstance(child, list):
              typeValue = renameWidgetMap[_key] if _key in renameWidgetMap else _key
              dataList.extend([{**each, '@type': typeValue} for each in child])
          item['children'] = process_children(dataList)
          children.append(item)
          if len(children):
            component['children'] = children
      else:
        children = []
        widget = element.get(key, None)
        component[key] = widget
        if isinstance(widget, list):
          for w in widget:
            if '@type' not in w:
              w['@type'] = key
            children.append(process_element(w))
        else:
          if '@type' not in widget:
            widget['@type'] = key
          children.append(process_element(widget))
        if len(children):
          component['children'] = children
    
    return component
  
  def process_children(elements):
    children = []
    if isinstance(elements, dict):
      children.append(process_element(elements))
    elif isinstance(elements, list):
      for element in elements:
        children.append(process_element(element))
    return children

  root:dict = xml_dict['template']
  scroll = root.get('@scroll', None)
  return process_element(root)['children'], scroll