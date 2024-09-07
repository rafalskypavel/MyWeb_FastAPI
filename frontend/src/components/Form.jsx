import React from 'react';
import { Button, Checkbox, Form, Input, message } from 'antd';
import axios from 'axios';
import qs from 'qs';

const MyForm = ({ onClose }) => {
  const onFinish = async (values) => {
    try {
      // Выводим данные в консоль перед отправкой
      console.log('Form values:', values);

      const response = await axios.post(
        'http://127.0.0.1:8000/auth/login',
        qs.stringify({
          username: values.username,
          password: values.password,
        }),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );
      console.log('Form submitted successfully:', response.data);
      onClose(); // Закрываем форму после успешной отправки
      message.success('Login successful');
    } catch (error) {
      console.error('Error submitting form:', error);
      message.error('Login failed');
    }
  };

  const onFinishFailed = (errorInfo) => {
    console.log('Failed:', errorInfo);
    message.error('Form submission failed');
  };

  return (
    <Form
      name="basic"
      labelCol={{ span: 8 }}
      wrapperCol={{ span: 16 }}
      style={{ maxWidth: 600 }}
      initialValues={{ remember: true }}
      onFinish={onFinish}
      onFinishFailed={onFinishFailed}
      autoComplete="off"
    >
      <Form.Item
        label="Username"
        name="username"
        rules={[{ required: true, message: 'Please input your username!' }]}
      >
        <Input />
      </Form.Item>

      <Form.Item
        label="Password"
        name="password"
        rules={[{ required: true, message: 'Please input your password!' }]}
      >
        <Input.Password />
      </Form.Item>

      <Form.Item name="remember" valuePropName="checked" wrapperCol={{ offset: 8, span: 16 }}>
        <Checkbox>Remember me</Checkbox>
      </Form.Item>

      <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
        <Button type="primary" htmlType="submit">Submit</Button>
        <Button onClick={onClose} style={{ marginLeft: 10 }}>Close</Button>
      </Form.Item>
    </Form>
  );
};

export default MyForm;
