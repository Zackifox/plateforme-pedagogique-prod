/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js}'],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: '#1d4ed8', hover: '#1e40af' },
      },
    },
  },
  plugins: [],
}
