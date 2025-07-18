# Fase 2 — Sistema de Autoatendimento Fast Food

## Visão Geral
Esta fase evolui o sistema para uma arquitetura hexagonal/clean, com regras de negócio robustas, validações avançadas, documentação rica em diagramas e suporte a deploy em produção e Kubernetes.

## Arquitetura
- **Hexagonal/Clean Architecture**: Separação clara entre domínio, casos de uso, adaptadores e infraestrutura.
- **DDD**: Entidades, agregados e repositórios bem definidos.
- **Validações e Policies**: Todas as regras de negócio críticas implementadas no domínio e use-cases.
- **Testes**: Scripts e estrutura prontos para validação automatizada.

## Diferenciais da Fase 2
- **Regras de negócio explícitas**: Policies como valor mínimo/máximo, estoque, horário, descontos, etc.
- **Validações avançadas**: CPF, email, nome, preço, quantidade, status, etc.
- **Event Storming detalhado**: Comandos, policies, fluxos alternativos e cenários de erro.
- **Fluxos alternativos mapeados**: Diagramas para todos os principais cenários de exceção.
- **Deploy profissional**: Docker multi-stage, Docker Compose, Kubernetes (manifests e kustomize).
- **Documentação visual**: Diagramas PlantUML e PNG.

## Como rodar
- Siga o README principal do projeto para instruções de ambiente, build, testes e deploy.
- Para deploy em produção/Kubernetes, utilize os manifests e scripts na pasta `backend/k8s`.

## Documentação desta fase
- `event-storming-fase2.puml`: Event Storming completo da fase 2
- `fluxos-alternativos.puml`: Fluxos alternativos e cenários de erro
- `architecture-fase2.puml`: Arquitetura detalhada da fase 2 (novo)

## Como evoluímos da fase 1
- Refatoração completa para clean architecture
- Policies e validações robustas em todos os use-cases
- Documentação ampliada e visual
- Pronto para produção e escalabilidade

---

> Para detalhes de cada regra, fluxo ou arquitetura, consulte os diagramas PlantUML nesta pasta. 