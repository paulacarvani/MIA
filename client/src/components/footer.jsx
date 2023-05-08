import { Facebook, Instagram, WhatsApp } from '@mui/icons-material';
import styled from 'styled-components'

const Container = styled.div`
    display: flex;
    flex-direction: column;
    padding: 20px;
    align-items: center;
    justify-content: center;
    background-color: #fcf5f5;
`;

const Name = styled.h1`
`;

const Desc = styled.p`
    margin: 20px 0px;
`;

const SocialContent = styled.div`
    display: flex;
`;

const SocialIcon = styled.div`
    width: 40px;
    height: 40px;
    border-radius: 50%;
    color: white;
    background-color: #${props=>props.color};
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 20px;
    cursor: pointer;
`;


const Footer = () => {
  return (
    <Container>
        <Name>ENSEÑEMOS A NUESTROS HIJOS A USAR LAS AI DE UNA FORMA RESPONSABLE</Name>
        <Desc>
            Proyecto creado por Paula Carvajal - Inspirado en mi hija Salomé
        </Desc>
        <SocialContent>
            <SocialIcon color="3B5999">
                <Facebook/>
            </SocialIcon>
            <SocialIcon color="E4405F">
                <Instagram/>
            </SocialIcon>
            <SocialIcon color="128c7e">
                <WhatsApp/>
            </SocialIcon>
        </SocialContent>
    </Container>
  )
}

export default Footer