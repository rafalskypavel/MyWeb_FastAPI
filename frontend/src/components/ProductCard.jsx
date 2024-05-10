import React from 'react';
import { Avatar, Card } from 'antd';
const { Meta } = Card;

function itemCard({ item }) {
  return (
    <Card
      style={{ width: 300, marginBottom: 100 }} // Добавляем marginBottom для разделения карточек
      cover={
<img
  alt={item.Name}
  src={item.Photo['image1']}
  style={{ objectFit: 'contain', width: '100%', height: 250 }} // Используем 'contain' для objectFit
/>

      }
      actions={[
        <span className="Price">{item.Price} {item.Сurrency}</span>,
        <span className="Id">Код товара: {item.Id}</span>,
        <a href={`https://www.pnevmoteh.ru`}>Подробнее</a>
      ]}
    >
      <Meta
        avatar={
          <Avatar
            src="https://www.pnevmoteh.ru/sites/pnevmoteh.ru/files/images/brands/frosp_logo_brend_0.svg"
            size={150}
            style={{ width: 80, height: 40 }}
          />
        }
          title={
            <div className="ant-card-meta-title" style={{ whiteSpace: 'normal' }}>
              {item.Name}
            </div>
          }
          description={item.description}
      />
    </Card>
  );
}

export default itemCard;
