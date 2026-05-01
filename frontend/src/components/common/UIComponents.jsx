import React from 'react';

export const Card = ({ children, className = '', title, action }) => {
  return (
    <div className={`fin-card p-5 ${className}`}>
      {(title || action) && (
        <div className="flex justify-between items-center mb-4">
          {title && <h3 className="font-semibold text-fin-text">{title}</h3>}
          {action && <div>{action}</div>}
        </div>
      )}
      {children}
    </div>
  );
};

export const Skeleton = ({ className = '' }) => {
  return (
    <div className={`animate-pulse bg-fin-border rounded-md ${className}`}></div>
  );
};

export const Spinner = ({ size = 'md' }) => {
  const sizeClasses = {
    sm: 'w-4 h-4 border-2',
    md: 'w-8 h-8 border-3',
    lg: 'w-12 h-12 border-4'
  };
  
  return (
    <div className="flex justify-center items-center p-4">
      <div className={`animate-spin rounded-full border-fin-border border-t-fin-blue ${sizeClasses[size]}`}></div>
    </div>
  );
};
