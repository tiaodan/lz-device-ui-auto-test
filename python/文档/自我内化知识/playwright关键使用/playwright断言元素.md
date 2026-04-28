"""验证元素可见性"""
        expect(self.username_input).to_be_visible() // 看输入框是否可见

"""验证元素可用性"""
        expect(self.username_input).to_be_enabled() // 看输入框是否可用

"""验证占位符文本"""
expect(self.username_input).to_have_attribute("placeholder", "Username")

"""验证滑块提示文本"""
expect(self.slider_text).to_contain_text("slide")

"""验证登录后 URL 变化"""
if expected_change:
    expect(self.page).not_to_have_url("/")
else:
    expect(self.page).to_have_url("/")