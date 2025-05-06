import React from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import {
  EffectCoverflow,
  Navigation,
  Pagination,
  Autoplay,
} from "swiper/modules";
import "swiper/css";
import "swiper/css/effect-coverflow";
import "swiper/css/pagination";
import "swiper/css/navigation";
import "swiper/css/autoplay";
import "./EventCarousel.css";

const EventCarousel = () => {
  const events = [
    {
      id: 1,
      title: "LAUANA PRADO RAIZ - TOUR 2025",
      image: "https://images.sympla.com.br/67867afacabb3.png",
      location: "Várias cidades",
      date: "Várias datas",
      link: "https://www.sympla.com.br/produtor/gtstalentbr",
    },
    {
      id: 2,
      title: "CUPOLA Summit 2025",
      image: "https://images.sympla.com.br/671bf74dd5ca8.png",
      location: "São Paulo - SP",
      date: "15-17 de Maio",
      link: "https://www.sympla.com.br/evento/cupola-summit-2025/2683898",
    },
    {
      id: 3,
      title: "MENINAS MALVADAS - O MUSICAL",
      image:
        "https://assets.bileto.sympla.com.br/eventmanager/production/3rp5jr60snpsbhp8cmcvltsdrv3gmdimk32c02ib1kvq0jve0bscoo3ek1cqhmcg7285c7t5djij5vj5fo0ka7vk859a6gmb8jgn1se.webp",
      location: "Rio de Janeiro - RJ",
      date: "Sábado, 15h",
      link: "https://bileto.sympla.com.br/event/99009",
    },
    {
      id: 4,
      title: "ExpoEcomm Curitiba 2025",
      image: "https://images.sympla.com.br/6761985a736f6.png",
      location: "Curitiba - PR",
      date: "10-12 de Julho",
      link: "https://www.sympla.com.br/evento/expoecomm-curitiba-2025/2773437",
    },
    {
      id: 5,
      title: "Victor Sarro em Goiânia/GO - Na Minha Época Não Era Bullying",
      image:
        "https://assets.bileto.sympla.com.br/eventmanager/production/3keh2enop5cpkh5q9p71g8odh4mu2ansqrgro3u6bp6fckipsfsahnfqf463iv90ltqagms9c13n2os9dh2nf2ta395nskbi4gndj1f.webp",
      location: "Goiânia - GO",
      date: "Sexta, 20h",
      link: "https://bileto.sympla.com.br/event/102581",
    },
    {
      id: 6,
      title: "Acústico NAVARANDA Goiânia",
      image: "https://images.sympla.com.br/679bb9d78cd60.jpg",
      location: "Goiânia - GO",
      date: "Sábado, 19h",
      link: "https://www.sympla.com.br/evento/acustico-navaranda-goiania/2815605",
    },
    {
      id: 7,
      title: "Leo Ritter em Espírita",
      image: "https://images.sympla.com.br/679e84c39fe3e.jpg",
      location: "Belo Horizonte - MG",
      date: "Domingo, 18h",
      link: "https://www.sympla.com.br/evento/leo-ritter-em-espirita/2791088",
    },
    {
      id: 8,
      title: "Congresso Científico Autismo Sem Fronteiras | Goiânia, Goiás.",
      image: "https://images.sympla.com.br/6781c90b2221a.png",
      location: "Goiânia - GO",
      date: "Sábado, 26 de Abr às 07:00",
      link: "https://www.sympla.com.br/evento/congresso-cientifico-autismo-sem-fronteiras-goiania-goias/2703249",
    },
  ];

  return (
    <div className="carousel-wrapper">
      <div className="event-carousel-sympla">
        <Swiper
          effect={"coverflow"}
          grabCursor={true}
          centeredSlides={true}
          slidesPerView={"auto"}
          initialSlide={Math.floor(events.length / 2)}
          autoplay={{
            delay: 3000,
            disableOnInteraction: false,
            pauseOnMouseEnter: true
          }}
          coverflowEffect={{
            rotate: 0,
            stretch: 100,
            depth: 300,
            modifier: 1,
            slideShadows: true,
          }}
          pagination={{
            clickable: true,
            el: ".custom-pagination",
          }}
          navigation={{
            nextEl: ".custom-next",
            prevEl: ".custom-prev",
          }}
          modules={[EffectCoverflow, Pagination, Navigation, Autoplay]}
          className="mySwiper"
          loop={true}
          speed={600}
        >
          {events.map((event) => (
            <SwiperSlide key={event.id}>
              <a href={event.link} className="sympla-card" target="_blank" rel="noopener noreferrer">
                <div
                  className="event-image"
                  style={{ backgroundImage: `url(${event.image})` }}
                ></div>
                <div className="event-info">
                  <h3 className="event-title">{event.title}</h3>
                  <div className="event-meta">
                    <span className="event-location">{event.location}</span>
                    <span className="event-date">{event.date}</span>
                  </div>
                </div>
              </a>
            </SwiperSlide>
          ))}
        </Swiper>
        <div className="custom-navigation">
          <div className="custom-prev">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path d="M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6 1.41-1.41z"/>
            </svg>
          </div>
          <div className="custom-next">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
              <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
            </svg>
          </div>
        </div>
        <div className="custom-pagination"></div>
      </div>
    </div>
  );
};

export default EventCarousel;
