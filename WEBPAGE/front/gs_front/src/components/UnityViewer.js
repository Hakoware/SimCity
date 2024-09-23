import React from 'react';

const UnityViewer = () => {
  return (
    <iframe
      src="http://localhost:3001/"
      style={{ width: '100%', height: '600px', border: 'none' }}
      title="Unity Game"
    ></iframe>
  );
};

export default UnityViewer;
