// App.jsx
import React, { useState, useEffect, useCallback } from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import axios from 'axios';
import { Layout, Menu, List, theme } from 'antd';
import { UserOutlined, VideoCameraOutlined, CloudOutlined, AppstoreOutlined, ShopOutlined } from '@ant-design/icons';
import ItemCard from './components/ProductCard';
import MyForm from './components/Form';
import MyPagination from './components/Pagination';
import CustomSearchInput from './components/SearchInput';

const { Header, Content, Footer, Sider } = Layout;

const menuItems = [
  { key: '1', icon: <UserOutlined />, label: 'Войти' },
  { key: '2', icon: <VideoCameraOutlined />, label: 'Корзина' },
  { key: '3', icon: <CloudOutlined />, label: 'Каталог' },
  { key: '4', icon: <AppstoreOutlined />, label: 'Избранное' },
  { key: '5', icon: <ShopOutlined />, label: 'О компании' },
];

const App = () => {
  const { colorBgContainer, borderRadiusLG } = theme.useToken().token;
  const [products, setProducts] = useState([]);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const [limit, setLimit] = useState(4);
  const [offset, setOffset] = useState(0);

const fetchFilteredProducts = async (filter) => {
  try {
    console.log('Filter query:', filter); // Log the filter query to check if it's correct
    const url = `http://127.0.0.1:8000/operations/filter?${filter}`;
    const response = await axios.get(url);
    setProducts(response.data);
  } catch (error) {
    console.error('Error fetching filtered products:', error);
  }
};


  const fetchProducts = useCallback(async () => {
    try {
      const url = `http://127.0.0.1:8000/operations/?limit=${limit}&offset=${offset}`;
      const response = await axios.get(url);
      setProducts(response.data.products_data);
      setTotalItems(response.data.total_count);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  }, [limit, offset]);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  const handleLimitChange = (newLimit) => {
    setLimit(newLimit);
    setOffset(0);
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
    setOffset((page - 1) * limit);
  };

  const handleNavClick = ({ key }) => {
    setIsFormOpen(key === '1');
  };

  const renderProducts = () => (
    <List
      grid={{ gutter: 33, xs: 1, sm: 2, md: 3, lg: 4, xl: 4, xxl: 4 }}
      dataSource={products}
      renderItem={(item) => (
        <List.Item>
          <ItemCard item={item} />
        </List.Item>
      )}
    />
  );

  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Sider width={180} style={{ overflow: 'auto', height: '100vh', position: 'fixed', left: 0 }}>
          <div className="logo" />
          <Menu theme="dark" mode="inline" defaultSelectedKeys={['3']} onClick={handleNavClick}>
            {menuItems.map(item => (
              <Menu.Item key={item.key} icon={item.icon}>
                {item.label}
              </Menu.Item>
            ))}
          </Menu>
        </Sider>
        <Layout style={{ marginLeft: 180 }}>
          <Header style={{ padding: 0, position: 'fixed', width: '100%', zIndex: 1000, background: colorBgContainer }}>
            <img
              src="https://www.pnevmoteh.ru/sites/pnevmoteh.ru/files/images/brands/frosp_logo_brend_0.svg"
              alt="Frosp Logo"
              style={{ width: 130, height: 50, display: 'inline-block', marginRight: 5 }}
            />
            <CustomSearchInput placeholder="Введите текст для поиска" onSearch={fetchFilteredProducts} style={{ width: 400, marginLeft: 5 }} />
          </Header>
          <Content style={{ margin: '80px 16px 0', overflow: 'initial' }}>
            <div style={{ padding: 24, textAlign: 'center', background: colorBgContainer, borderRadius: borderRadiusLG }}>
              {isFormOpen ? <MyForm onClose={() => setIsFormOpen(false)} /> : renderProducts()}
            </div>
            {!isFormOpen && (
              <MyPagination
                currentPage={currentPage}
                handlePageChange={handlePageChange}
                handleLimitChange={handleLimitChange}
                totalItems={totalItems}
                limit={limit}
              />
            )}
          </Content>
          <Footer style={{ textAlign: 'center' }}>Ant Design ©{new Date().getFullYear()} Created by Ant UED</Footer>
        </Layout>
      </Layout>
    </Router>
  );
};

export default App;
