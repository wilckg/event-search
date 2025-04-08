import React, { useRef } from "react";
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
  // const swiperRef = useRef(null);;

  // Dados dos eventos simulando a API do Sympla
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
            stretch: 0,
            depth: 200,
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
          breakpoints={{
            640: {
              coverflowEffect: {
                depth: 100
              }
            }
          }}
        >
          {events.map((event) => (
            <SwiperSlide key={event.id}>
              <a href={event.link} className="sympla-card">
                <div
                  className="event-image"
                  style={{ backgroundImage: `url(${event.image})` }}
                ></div>
                <div className="event-info">
                  <h3 className="event-title">{event.title}</h3>
                  <div className="event-meta">
                    <span className="event-location">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        width="1em"
                        height="1em"
                      >
                        <path
                          fill="currentColor"
                          fillRule="evenodd"
                          d="M4 9.92a8 8 0 1 1 16 0c0 5.48-7 11.58-7.35 11.84a1 1 0 0 1-1.3 0C11.05 21.5 4 15.4 4 9.92m8 9.73c-1.68-1.59-6-6-6-9.73a6 6 0 1 1 12 0c0 3.69-4.32 8.14-6 9.73M8.5 9.5a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0m2 0a1.5 1.5 0 1 0 3 0 1.5 1.5 0 0 0-3 0"
                          clipRule="evenodd"
                        ></path>
                      </svg>
                      {event.location}
                    </span>
                    <span className="event-date">
                      <svg
                        viewBox="0 0 20 20"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <g clipPath="url(#a)">
                          <path
                            d="M17.5 8.334h-15m10.833-6.667V5M6.667 1.667V5M6.5 18.334h7c1.4 0 2.1 0 2.635-.273a2.5 2.5 0 0 0 1.092-1.092c.273-.535.273-1.235.273-2.635v-7c0-1.4 0-2.1-.273-2.635a2.5 2.5 0 0 0-1.092-1.093c-.535-.272-1.235-.272-2.635-.272h-7c-1.4 0-2.1 0-2.635.272A2.5 2.5 0 0 0 2.772 4.7C2.5 5.233 2.5 5.934 2.5 7.334v7c0 1.4 0 2.1.272 2.635a2.5 2.5 0 0 0 1.093 1.092c.535.273 1.235.273 2.635.273Z"
                            stroke="#717680"
                            strokeWidth="1.8"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                          ></path>
                        </g>
                        <defs>
                          <clipPath id="a">
                            <path fill="#fff" d="M0 0h20v20H0z"></path>
                          </clipPath>
                        </defs>
                      </svg>
                      {event.date}
                    </span>
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
