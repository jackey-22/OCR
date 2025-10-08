import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';
import 'primeicons/primeicons.css';
// import 'primereact/resources/themes/lara-light-blue/theme.css';
// import 'primereact/resources/primereact.min.css';
import { PrimeReactProvider } from 'primereact/api';

ReactDOM.createRoot(document.getElementById('root')).render(
	<PrimeReactProvider value={{ ripple: true }}>
		<App />
	</PrimeReactProvider>
);
