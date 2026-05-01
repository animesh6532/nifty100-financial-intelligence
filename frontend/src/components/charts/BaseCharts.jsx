import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  RadialLinearScale,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line, Bar, Radar, Doughnut } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale, LinearScale, PointElement, LineElement, BarElement, RadialLinearScale,
  Title, Tooltip, Legend, Filler
);

// Global Chart defaults for dark theme
ChartJS.defaults.color = '#94a3b8';
ChartJS.defaults.borderColor = '#1e293b';
ChartJS.defaults.font.family = 'Inter';

const commonOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
      labels: { boxWidth: 12, usePointStyle: true }
    },
    tooltip: {
      backgroundColor: '#131b2c',
      titleColor: '#f8fafc',
      bodyColor: '#e2e8f0',
      borderColor: '#1e293b',
      borderWidth: 1,
      padding: 10,
    }
  }
};

export const LineChart = ({ data, options = {} }) => {
  return <Line data={data} options={{ ...commonOptions, ...options }} />;
};

export const BarChart = ({ data, options = {} }) => {
  return <Bar data={data} options={{ ...commonOptions, ...options }} />;
};

export const RadarChart = ({ data, options = {} }) => {
  return (
    <Radar 
      data={data} 
      options={{
        ...commonOptions,
        scales: {
          r: {
            angleLines: { color: '#1e293b' },
            grid: { color: '#1e293b' },
            pointLabels: { color: '#94a3b8' },
            ticks: { backdropColor: 'transparent', color: 'transparent' }
          }
        },
        ...options
      }} 
    />
  );
};
