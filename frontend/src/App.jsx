import React, { useEffect, useState } from 'react';
import { Pagination, List, Card, Layout, Menu, theme , Avatar} from 'antd';
import {
  AppstoreOutlined,
  BarChartOutlined,
  CloudOutlined,
  ShopOutlined,
  TeamOutlined,
  UploadOutlined,
  UserOutlined,
  VideoCameraOutlined,
} from '@ant-design/icons';
import axios from 'axios';
import { EditOutlined, EllipsisOutlined, SettingOutlined, MoreOutlined } from '@ant-design/icons';
import ProductCard from './components/ProductCard';
const { Header, Content, Footer, Sider } = Layout;
const { Meta } = Card;

const items = [
  UserOutlined,
  VideoCameraOutlined,
  UploadOutlined,
  BarChartOutlined,
  CloudOutlined,
  AppstoreOutlined,
  TeamOutlined,
  ShopOutlined,
].map((icon, index) => ({
  key: String(index + 1),
  icon: React.createElement(icon),
  label: `nav ${index + 1}`,
}));

const itemRender = (_, type, originalElement) => {
  if (type === 'prev') {
    return <a>Previous</a>;
  }
  if (type === 'next') {
    return <a>Next</a>;
  }
  return originalElement;
};

const App = () => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const [products, setProducts] = useState([]);

  const fetchProducts = () => {
    axios.get('http://127.0.0.1:8000/operations/').then((response) => {
      console.log('Response:', response.data);
      setProducts(response.data);
    }).catch((error) => {
      console.error('Error fetching products:', error);
    });
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  return (
    <Layout hasSider>
      <Sider
        style={{
          overflow: 'auto',
          height: '100vh',
          position: 'fixed',
          left: 0,
          top: 0,
          bottom: 0,
        }}
      >
        <div className="demo-logo-vertical" />
        <Menu theme="dark" mode="inline" defaultSelectedKeys={['4']} items={items} />
      </Sider>
      <Layout
        style={{
          marginLeft: 200,
        }}
      >
        <Header
          style={{
            padding: 0,
            background: colorBgContainer,
          }}
        />

        <Content
          style={{
            margin: '24px 16px 0',
            overflow: 'initial',
          }}
        >
          <div
            style={{
              padding: 24,
              textAlign: 'center',
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >

            <List
              grid={{ gutter: 16, xs: 1, sm: 2, md: 2, lg: 3, xl: 3, xxl: 4 }}
              dataSource={products}
              renderItem={(item) => (
                <List.Item>
                  <ProductCard item={item} /> {/* Замените Card на ProductCard и передайте item как пропс */}
                </List.Item>
              )}
            />

                />
            />


            {/* Добавляем Pagination */}
            <Pagination total={500} itemRender={itemRender} />
          </div>
        </Content>

        <Footer
          style={{
            textAlign: 'center',
          }}
        >
          Ant Design ©{new Date().getFullYear()} Created by Ant UED
        </Footer>
      </Layout>
    </Layout>
  );
};

export default App;
