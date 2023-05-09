import React from 'react'
import styled from 'styled-components'

const Container = styled.div`
    height: 100px;
    background-image: url('https://img.freepik.com/vector-gratis/dia-nino-dibujado-mano-fondo-espanol_23-2149299345.jpg?w=740&t=st=1683597715~exp=1683598315~hmac=7a36ef9f02c38e198370db4fc6fa33c848b55daeabcd7b7647777f78c9beaa2d');
`;

const Wrapper =styled.div`
    padding: 50px 50px;
    display: flex;
    align-items: center;
`;


const Logo = styled.div`
    padding: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: auto;
    font-size: 40px;
    color: #4DCDD1;
    text-shadow: 1px 1px #fff;
`;


const Navbar = () => {
    return (
    <Container>
        <Wrapper>
            <Logo><img src = 'https://i.ibb.co/mGKY5mY/MIALogo.png' />Tu primera Inteligencia Artificial</Logo>
        </Wrapper>
    </Container>
    )
}

export default Navbar