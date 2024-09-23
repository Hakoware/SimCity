import React from 'react';
import dinero_emoji from '../assets/images/dinero_emoji.png'

const Pricing = () => {
  return (
    <div>
      <h1>Presios</h1>
      <div style={{ display: 'grid', placeItems: 'center', height: '100vh' }}>
        <img src={dinero_emoji} alt="Dineros" style={{ width: '300px', height: 'auto' }} />
      </div>
      
    </div>
  );
};

export default Pricing;