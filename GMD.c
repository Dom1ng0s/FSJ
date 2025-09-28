#include <stdio.h>
#include <stdlib.h> 
#include <math.h>
void Clear() {
    #ifdef _WIN32
        system("cls");
    #else
        system("clear");
    #endif
}

void TempoNaFazenda()
{
    int INWeight,DesFinWeight;
    float GMD;
    puts("Por favor insira o Peso Inicial:");
    scanf("%d",&INWeight);
    puts("Por favor insira o Peso Final Desejado:");
    scanf("%d",&DesFinWeight);
    puts("Por favor insira o GMD médio da Fazenda em Kg");
    scanf("%f",&GMD);
    int NeedWeight = DesFinWeight - INWeight;
    float Meses = (float) NeedWeight/(GMD*30);
    printf("Resultado:\n");
    printf("+--------------+-------------------+--------------+---------+---------+\n");
    printf("| Peso Inicial | Peso Final Desej. | GMD (Kg/dia) | Ganho   | Meses   |\n");
    printf("+--------------+-------------------+--------------+---------+---------+\n");
    printf("| %12d | %17d | %12.2f | %7d | %7.1f |\n", INWeight, DesFinWeight, GMD, NeedWeight, Meses);
    printf("+--------------+-------------------+--------------+---------+---------+\n");
    printf("Pressione ENTER para continuar...\n");
    getchar(); getchar(); // Aguarda ENTER
    Clear();
}

void CalcGMD()
{
    int INWeight,FINWeight;
    int  Duracao_meses;
    puts("Por favor insira o Peso Inicial:");
    scanf("%d",&INWeight);
    puts("Por favor insira o Peso Final:");
    scanf("%d",&FINWeight);
    puts("Por favor insira o tempo que o Animal passou na fazenda em Meses:");
    scanf("%d",&Duracao_meses);
    float GMD = (float) (FINWeight - INWeight) / (Duracao_meses*30);
    printf("+--------------+------------+-------------------+---------+\n");
    printf("| Peso Inicial | Peso Final | Tempo em Meses    |   GMD   |\n");
    printf("+--------------+------------+-------------------+---------+\n");
    printf("| %12d | %10d | %17d | %7.2f |\n", INWeight, FINWeight, Duracao_meses, GMD);
    printf("+--------------+------------+-------------------+---------+\n");
    printf("Pressione ENTER para continuar...\n");
    getchar(); getchar(); // Aguarda ENTER
    Clear();
}

int main()
{
    int opcao;
    do {
        printf("\n===== MENU PRINCIPAL =====\n");
        printf("1 - Calcular Tempo na Fazenda\n");
        printf("2 - Calcular GMD\n");
        printf("3 - Tutorial\n");
        printf("0 - Sair\n");
        printf("Escolha uma opção: ");
        scanf("%d", &opcao);

        switch(opcao) {
            case 1:
                TempoNaFazenda();
                break;
            case 2:
                CalcGMD();
                break;
            case 3:
                printf("\n--- Tutorial ---\n");
                printf("1. Calcular Tempo na Fazenda:\n");
                printf("   Informe o peso inicial, peso final desejado e o GMD médio.\n");
                printf("   O programa mostrará quantos meses são necessários para atingir o peso desejado.\n\n");
                printf("2. Calcular GMD:\n");
                printf("   Informe o peso inicial, peso final e o tempo em meses.\n");
                printf("   O programa calculará o ganho médio diário (GMD).\n\n");
                printf("Pressione ENTER para voltar ao menu...\n");
                getchar(); getchar(); // Aguarda ENTER
                Clear();
                break;
            case 0:
                printf("Saindo...\n");
                break;
            default:
                printf("Opção inválida!\n");
        }
    } while(opcao != 0);

    return 0;
}
