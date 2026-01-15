# Orienta - Guia de Identidade Visual

Este documento define a identidade visual do Orienta para garantir consistência em todas as páginas e componentes da aplicação.

---

## 📋 Índice

1. [Paleta de Cores](#paleta-de-cores)
2. [Tipografia](#tipografia)
3. [Espaçamento](#espaçamento)
4. [Componentes](#componentes)
5. [Layout](#layout)
6. [Animações](#animações)
7. [Responsividade](#responsividade)
8. [Ícones e Imagens](#ícones-e-imagens)

---

## 🎨 Paleta de Cores

### Cores Principais

| Nome           | Hex       | Tailwind Class      | Uso                                 |
| -------------- | --------- | ------------------- | ----------------------------------- |
| Background     | `#f5f5f5` | `bg-[#f5f5f5]`      | Fundo principal das páginas         |
| Branco         | `#ffffff` | `bg-white`          | Cards, modais, elementos flutuantes |
| Azul Principal | `#3b82f6` | `bg-blue-500`       | Botões primários, CTAs              |
| Azul Hover     | `#2563eb` | `hover:bg-blue-600` | Estado hover de botões primários    |

### Cores de Texto

| Nome             | Hex       | Tailwind Class  | Uso                               |
| ---------------- | --------- | --------------- | --------------------------------- |
| Texto Primário   | `#111827` | `text-gray-900` | Títulos, textos importantes       |
| Texto Secundário | `#4b5563` | `text-gray-600` | Navegação, links, textos de apoio |
| Texto Terciário  | `#6b7280` | `text-gray-500` | Subtítulos, descrições            |
| Texto Muted      | `#9ca3af` | `text-gray-400` | Títulos secundários, placeholders |

### Cores de Destaque

| Nome            | Hex       | Tailwind Class  | Uso                        |
| --------------- | --------- | --------------- | -------------------------- |
| Amarelo         | `#fef9c3` | `bg-yellow-100` | Sticky notes, destaques    |
| Vermelho Accent | `#f87171` | `bg-red-400`    | Pins, notificações         |
| Cinza Claro     | `#f3f4f6` | `bg-gray-100`   | Placeholders, áreas vazias |

---

## 🔤 Tipografia

### Família de Fontes

```css
/* Font principal */
font-family:
    system-ui,
    -apple-system,
    sans-serif;

/* Font para marca/logo */
font-family: serif; /* Tailwind: font-serif */
```

### Tamanhos de Fonte

| Elemento            | Mobile | Desktop | Tailwind Class         |
| ------------------- | ------ | ------- | ---------------------- |
| Título H1           | 48px   | 60px    | `text-5xl md:text-6xl` |
| Título H2           | 48px   | 60px    | `text-5xl md:text-6xl` |
| Logo/Marca          | 20px   | 20px    | `text-xl`              |
| Parágrafo           | 18px   | 18px    | `text-lg`              |
| Navegação           | 16px   | 16px    | `text-base` (padrão)   |
| Labels Pequenos     | 14px   | 14px    | `text-sm`              |
| Texto Muito Pequeno | 12px   | 12px    | `text-xs`              |

### Pesos de Fonte

| Peso     | Tailwind Class  | Uso                         |
| -------- | --------------- | --------------------------- |
| Bold     | `font-bold`     | Títulos, CTAs, marca        |
| Semibold | `font-semibold` | Subtítulos de cards, botões |
| Normal   | `font-normal`   | Texto corrido               |

### Estilos de Texto

```jsx
// Itálico para destaques suaves
<em>planos de estudo personalizados</em>

// Negrito para ênfase forte
<strong>seu ritmo</strong>
```

---

## 📐 Espaçamento

### Sistema de Grid

- **Container máximo:** `max-w-7xl` (1280px)
- **Centralização:** `mx-auto`
- **Padding horizontal:** `px-8` (32px)

### Margens e Paddings Padrão

| Uso                     | Classe       | Valor       |
| ----------------------- | ------------ | ----------- |
| Gap pequeno             | `gap-2`      | 8px         |
| Gap médio               | `gap-4`      | 16px        |
| Gap grande              | `gap-8`      | 32px        |
| Gap extra grande        | `gap-12`     | 48px        |
| Padding de seção        | `pt-24 pb-8` | 96px / 32px |
| Padding de cards        | `p-4`        | 16px        |
| Margin bottom título    | `mb-2`       | 8px         |
| Margin bottom subtítulo | `mb-8`       | 32px        |
| Margin bottom parágrafo | `mb-10`      | 40px        |

---

## 🧩 Componentes

### Header

```jsx
<header className="flex items-center justify-between px-8 py-4 max-w-7xl mx-auto">
```

**Estrutura:**

1. Logo + Nome da marca (esquerda)
2. Navegação central (hidden em mobile)
3. Ações do usuário (direita)

**Estilos específicos:**

- Padding vertical: `py-4` (16px)
- Padding horizontal: `px-8` (32px)
- Layout: `flex items-center justify-between`

### Logo

```jsx
<div className="flex items-center gap-2">
    <div className="w-8 h-8 flex items-center justify-center">
        <img src="/public/compass.png" alt="Orienta Logo" />
    </div>
    <span className="font-serif font-bold text-xl">Orienta</span>
</div>
```

**Especificações:**

- Tamanho do ícone: `w-8 h-8` (32x32px)
- Gap entre ícone e texto: `gap-2` (8px)
- Fonte do nome: `font-serif font-bold text-xl`

### Navegação

```jsx
<nav className="hidden md:flex items-center gap-8">
    <a
        href="#section"
        className="text-gray-600 hover:text-gray-900 transition-colors"
    >
        Link
    </a>
</nav>
```

**Estilos de links:**

- Cor padrão: `text-gray-600`
- Cor hover: `hover:text-gray-900`
- Transição: `transition-colors`
- Espaçamento: `gap-8` (32px)

### Botões

#### Botão Primário (CTA)

```jsx
<Button
    className="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-8 py-6 rounded-full text-lg"
    size="lg"
>
    Texto do Botão
</Button>
```

**Especificações:**

- Background: `bg-blue-500`
- Hover: `hover:bg-blue-600`
- Texto: `text-white font-semibold text-lg`
- Padding: `px-8 py-6` (32px / 24px)
- Border radius: `rounded-full`

#### Botão Secundário (Outline)

```jsx
<Button variant="outline" className="rounded-full">
    Texto do Botão
</Button>
```

**Especificações:**

- Variante: `outline`
- Border radius: `rounded-full`

### Cards Flutuantes

```jsx
<div className="hidden lg:block absolute [position] w-48 bg-white rounded-xl shadow-lg p-4 z-10">
    {/* Conteúdo */}
</div>
```

**Estilos base:**

- Background: `bg-white`
- Border radius: `rounded-xl` (12px)
- Sombra: `shadow-lg`
- Padding: `p-4` (16px)
- Z-index: `z-10`
- Visibilidade: `hidden lg:block` (apenas desktop)

### Sticky Note

```jsx
<div className="hidden lg:block absolute top-8 left-8 w-48 h-40 bg-yellow-100 rounded-lg shadow-lg p-4 rotate-[-5deg] z-10">
    <div className="w-3 h-3 bg-red-400 rounded-full absolute -top-1 left-1/2 -translate-x-1/2"></div>
    {/* Conteúdo */}
</div>
```

**Especificações:**

- Background: `bg-yellow-100`
- Dimensões: `w-48 h-40` (192px x 160px)
- Rotação: `rotate-[-5deg]`
- Pin: círculo vermelho centralizado no topo

---

## 📱 Layout

### Estrutura da Página

```jsx
<div className="min-h-screen bg-[#f5f5f5] w-full">
    <header>...</header>
    <main className="relative max-w-7xl mx-auto px-8 pt-8 pb-24">
        {/* Elementos flutuantes (absolute) */}
        {/* Conteúdo central (relative z-20) */}
    </main>
</div>
```

### Hero Section

```jsx
<div className="flex flex-col items-center text-center pt-24 pb-8 relative z-20">
    {/* Ícone/Logo */}
    {/* Título Principal */}
    {/* Subtítulo */}
    {/* Descrição */}
    {/* CTA */}
</div>
```

**Especificações:**

- Alinhamento: `flex flex-col items-center text-center`
- Padding: `pt-24 pb-8`
- Z-index: `z-20` (acima dos elementos flutuantes)

### Hierarquia de Z-index

| Elemento             | Z-index | Classe |
| -------------------- | ------- | ------ |
| Elementos flutuantes | 10      | `z-10` |
| Conteúdo principal   | 20      | `z-20` |

---

## ✨ Animações

### Classes de Animação

```css
/* Definir no globals.css ou tailwind.config.js */
.animate-fade-in {
    animation: fadeIn 0.6s ease-out forwards;
}

.animation-delay-100 {
    animation-delay: 100ms;
}

.animation-delay-200 {
    animation-delay: 200ms;
}

.animation-delay-300 {
    animation-delay: 300ms;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

### Uso das Animações

| Elemento  | Classe                                | Delay |
| --------- | ------------------------------------- | ----- |
| Título H1 | `animate-fade-in`                     | 0ms   |
| Título H2 | `animate-fade-in animation-delay-100` | 100ms |
| Parágrafo | `animate-fade-in animation-delay-200` | 200ms |
| Botão CTA | `animate-fade-in animation-delay-300` | 300ms |

### Transições

```jsx
// Para mudanças de cor
className = "transition-colors";

// Duração padrão: 150ms (Tailwind default)
```

---

## 📱 Responsividade

### Breakpoints (Tailwind)

| Nome    | Largura Mínima | Prefixo  |
| ------- | -------------- | -------- |
| Mobile  | 0px            | (padrão) |
| Tablet  | 768px          | `md:`    |
| Desktop | 1024px         | `lg:`    |

### Regras de Responsividade

1. **Navegação:**
    - Mobile: `hidden`
    - Tablet+: `md:flex`

2. **Elementos flutuantes:**
    - Mobile/Tablet: `hidden`
    - Desktop: `lg:block`

3. **Títulos:**
    - Mobile: `text-5xl` (48px)
    - Desktop: `md:text-6xl` (60px)

### Exemplo de Componente Responsivo

```jsx
// Navegação responsiva
<nav className="hidden md:flex items-center gap-8">
    {/* Links */}
</nav>

// Card flutuante responsivo
<div className="hidden lg:block absolute ...">
    {/* Conteúdo */}
</div>
```

---

## 🖼️ Ícones e Imagens

### Logo/Ícone Principal

- **Arquivo:** `/public/compass.png`
- **Tamanhos de uso:**
    - Header: `w-8 h-8` (32x32px)
    - Hero central: `w-16 h-16` (64x64px)

### Placeholder para Imagens

```jsx
<div className="h-16 bg-gray-100 rounded flex items-center justify-center text-xs text-gray-400">
    Placeholder: Descrição da Imagem
</div>
```

**Estilos:**

- Background: `bg-gray-100`
- Border radius: `rounded`
- Texto: `text-xs text-gray-400`
- Layout: `flex items-center justify-center`

---

## 📝 Checklist para Novas Páginas

Ao criar uma nova página, verifique:

- [ ] Background principal: `bg-[#f5f5f5]`
- [ ] Container com `max-w-7xl mx-auto px-8`
- [ ] Header consistente com logo e navegação
- [ ] Cores de texto seguindo a hierarquia definida
- [ ] Botões usando os estilos padronizados
- [ ] Animações `animate-fade-in` nos elementos principais
- [ ] Responsividade para mobile, tablet e desktop
- [ ] Z-index correto para sobreposições

---

## 🔧 Configuração do Tailwind

Adicionar ao `tailwind.config.js` se necessário:

```javascript
module.exports = {
    theme: {
        extend: {
            colors: {
                background: "#f5f5f5",
            },
            animation: {
                "fade-in": "fadeIn 0.6s ease-out forwards",
            },
            keyframes: {
                fadeIn: {
                    "0%": { opacity: "0", transform: "translateY(10px)" },
                    "100%": { opacity: "1", transform: "translateY(0)" },
                },
            },
        },
    },
};
```

---

_Última atualização: Janeiro 2026_
