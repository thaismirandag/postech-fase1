# Documentação do Projeto

## Diagramas

### Arquitetura do Sistema

O diagrama de arquitetura do sistema está disponível no arquivo `architecture.puml`. Para visualizar este diagrama, você pode:

1. Usar a extensão PlantUML no VS Code
2. Usar o [PlantUML Online Server](http://www.plantuml.com/plantuml/uml/)
3. Usar o [PlantUML Viewer](https://plantuml.com/plantuml/uml/)

### Como Visualizar

1. Instale a extensão PlantUML no VS Code
2. Abra o arquivo `architecture.puml`
3. Pressione `Alt+D` para visualizar o diagrama

### Estrutura do Diagrama

O diagrama de arquitetura representa:

- Frontend (Interfaces do Cliente e Administrativa)
- Backend (Camadas da Arquitetura Hexagonal)
  - API Layer
  - Application Layer
  - Domain Layer
  - Infrastructure Layer
- Banco de Dados PostgreSQL
- Integração com Mercado Pago

### Notas Importantes

- O diagrama segue os princípios da Arquitetura Hexagonal
- As setas indicam as dependências entre os componentes
- As notas contêm informações adicionais sobre endpoints e tabelas 