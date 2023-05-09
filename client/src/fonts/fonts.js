import { createGlobalStyle } from 'styled-components';

import UniSansBoldRegular from '../fonts/UniSansBoldRegular.ttf';

export default createGlobalStyle`
    @font-face {
        font-family: 'Font Name';
        src: local('Font Name'), local('FontName'),
        url(${UniSansBoldRegular}) format('woff2'),
        font-weight: 300;
        font-style: normal;
    }
`;