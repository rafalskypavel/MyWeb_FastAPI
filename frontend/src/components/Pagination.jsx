// стартовая
import React from 'react';
import { Pagination, Select } from 'antd';

const { Option } = Select;

const PAGE_SIZE_OPTIONS = [4, 8, 16, 32]; // Константы для значений размеров страницы

const MyPagination = ({ currentPage, handlePageChange, handleLimitChange, totalItems, limit }) => {
  const itemRender = (_, type, originalElement) => {
    if (type === 'prev') {
      return <a className="ant-pagination-item-link">Previous</a>;
    }
    if (type === 'next') {
      return <a className="ant-pagination-item-link">Next</a>;
    }
    return originalElement;
  };

  const handlePageSizeChange = (value) => {
    handleLimitChange(parseInt(value)); // Обновляем limit в App компоненте
  };

  return (
    <div className="my-pagination" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginTop: 16 }}>
      <Pagination
        total={totalItems}
        current={currentPage}
        pageSize={limit}
        onChange={handlePageChange}
        itemRender={itemRender}
        showSizeChanger={false} // Отключаем встроенный выбор количества элементов на странице
      />
      <Select
        defaultValue={`${limit}`}
        style={{ marginLeft: 16, width: 120 }}
        onChange={handlePageSizeChange}
      >
        {PAGE_SIZE_OPTIONS.map(option => (
          <Option key={option} value={option}>{option} / page</Option>
        ))}
      </Select>
    </div>
  );
};

export default MyPagination;
