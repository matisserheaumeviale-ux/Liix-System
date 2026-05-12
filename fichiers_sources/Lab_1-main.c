/* USER CODE BEGIN Header */
/********************************************************************************
  Fichier:       Lab_1.zip

  Description: - Laboratoire 1 programme 1 
               - Afficher : "Bonjour Toi" 
									et fait flasher le LED D1 de la carte BluePill aux 1/2 sec. 

  En Entree:   - Aucune.
                 

  En Sortie:   - Message "Bonjour Toi" qui s'affiche � l'�cran.
                 


  Programmeur: Francois Bouchard
                Yunis

  Date:        12/12/2024

  Compilateur: IAR for ARM  v8.50.1

  Modification:
*******************************************************************************/
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

#include <_DeclarationGenerale.h>
#include "printf-scanf.h"
#include "PORT_1-2.h"
#include "stdbool.h"
#include "lcd.h"

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
UART_HandleTypeDef huart1;

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_USART1_UART_Init(void);
/* USER CODE BEGIN PFP */
void vDelaiMs(unsigned int uiDelai);
void vChaser(void);
void vDice(void);
/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */
	
  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */
 
  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USART1_UART_Init();
  /* USER CODE BEGIN 2 */
  LCD_Init();
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
   LCD_SetCursor(0,0);
   LCD_SendString("Bonjour Toi");

  bool bNouvelEtat = bReadPin(2,2);
  bool bAncienEtat = bReadPin(2,2);
  while (1)
  {
    bNouvelEtat = bReadPin(2,2);
    
    if (bNouvelEtat != bAncienEtat){
     bAncienEtat = bNouvelEtat;
      while(bNouvelEtat == 0){
        vDice();
        vDelaiMs(250);
        bNouvelEtat = bReadPin(2,2);
      }
    }
    

		
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.HSEPredivValue = RCC_HSE_PREDIV_DIV2;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL13;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief USART1 Initialization Function
  * @param None
  * @retval None
  */


/* USER CODE BEGIN 4 */
//*********************************vDelaiMs**************************
// Nom de la fonction : vDelaiMs
// Auteur : Yunis Sebany
// Date de création : 06-02-2026
// Date de la dernière modification : 06-02-2026
// Description : Fonction pour creer un delai en ms sur processeur 8mhz
// 
// Prototype: void vDelaiMs(unsigned int uiDelai)
//
// Appel :vDelai(1000);
// Permet de faire un delai de 1 seconde.
//
// Fonctions appelées : Aucun
// Paramètres d'entrée : uiDelai
// Paramètres de sortie : Aucun
// Variables utilisées : uidelaiOut, uiDelaiIn, uiDelai
// Equate : Aucun
// #Define : Aucun
// 
//******************************************************************
void vDelaiMs(unsigned int uiDelai){
  unsigned int uiDelaiOut = 0;
  while(uiDelaiOut < uiDelai){
    uiDelaiOut++;
    unsigned int uiDelaiIn = 0;
    while(uiDelaiIn < 8500){
      uiDelaiIn++;
    }
  }
}


//*********************************vDelaiMs**************************
// Nom de la fonction : vChaser
// Auteur : Yunis Sebany
// Date de création : 06-02-2026
// Date de la dernière modification : 06-02-2026
// Description : Chenillard sur 8bits
// 
// Prototype: void vChaser(void)
//
// Appel :vChaser();
// Lance le chenillard.
//
// Fonctions appelées : vWritePort, vDelaiMs
// Paramètres d'entrée : Aucun
// Paramètres de sortie : Aucun
// Variables utilisées : ucPort1, ucMask
// Equate : Aucun
// #Define : Aucun
// 
//******************************************************************
void vChaser(void){
  	static unsigned char ucPort1 = 0x7F;  //variable static afin de conserver sa valeur tout en limitant son scope a la fonction vChaser
    static unsigned char ucMask = 0x80;
  if(ucPort1 != 0xFE){
    ucPort1 = (0xFF ^ ucMask); 
    ucMask = ucMask >> 1;
  } else { 
    ucPort1 = 0x7F;
    ucMask = 0x80;
  } 
  vWritePort( ucPort1 , 1 ); 
  vDelaiMs(500); 
 
  ucPort1 = (unsigned char)((GPIOA->IDR >> 1) & 0xFF); 
}




//*********************************vDice**************************
// Nom de la fonction : vChaser
// Auteur : Yunis Sebany
// Date de création : 06-02-2026
// Date de la dernière modification : 06-02-2026
// Description : affiche sur les dels la valeur du De
// 
// Prototype: void vDice(void)
//
// Appel :vDice();
// Lance le chenillard.
//
// Fonctions appelées : vWritePort
// Paramètres d'entrée : Aucun
// Paramètres de sortie : Aucun
// Variables utilisées : ucnumber[], i
// Equate : Aucun
// #Define : Aucun
// 
//******************************************************************
void vDice(void){
  static unsigned char ucNumber[6] = {0xE, 0x7, 0xA, 0x9, 0x8, 0x1}; // static afin de ne pas recreer le tableau et el limiter a la fonction
  static char i = 0; //index pour le tableau
    if (i > 5){
      i = 0;
    }
    vWritePort(ucNumber[i] & 0xF, 1);
   i++;
}

