/* USER CODE BEGIN Header */
/********************************************************************************
  Fichier:   Lab2.zip    

  Description: Fonction Factoriel, et delai en ms
                
									 

  En Entree:   
                 

  En Sortie:   
                 


  Programmeur: Yunis Sebany

  Date:        13-02-26

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
#include <stdio.h>
#include <stdbool.h>

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
unsigned int factoriel(unsigned int iNumber);
void msDelay(unsigned int uiDelay);
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
  uint32_t clock = SystemCoreClock;
  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USART1_UART_Init();
  /* USER CODE BEGIN 2 */
  LCD_Init();
  LCD_SetCursor(0,0);
  LCD_Clear();
  LCD_SendString("Factoriel");
  LCD_SetCursor(0,1);

  unsigned int uiNumber =8;
  char buf[19];
  sprintf(buf,"!%d", clock);
  LCD_SendString(buf);

  unsigned int uiResult = factoriel(uiNumber);
  char str[19];
  sprintf(str, "=%d", uiResult);
  LCD_SetCursor(0,3);
  LCD_SendString(str);
  bool bLed = 0;
/* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */
    bLed ^= 1;
    vWritePin(2,5,bLed);
    msDelay(100);
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
static void MX_USART1_UART_Init(void)
{

  /* USER CODE BEGIN USART1_Init 0 */

  /* USER CODE END USART1_Init 0 */

  /* USER CODE BEGIN USART1_Init 1 */

  /* USER CODE END USART1_Init 1 */
  huart1.Instance = USART1;
  huart1.Init.BaudRate = 19200;
  huart1.Init.WordLength = UART_WORDLENGTH_8B;
  huart1.Init.StopBits = UART_STOPBITS_1;
  huart1.Init.Parity = UART_PARITY_NONE;
  huart1.Init.Mode = UART_MODE_TX_RX;
  huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart1.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART1_Init 2 */

  /* USER CODE END USART1_Init 2 */

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};
/* USER CODE BEGIN MX_GPIO_Init_1 */
/* USER CODE END MX_GPIO_Init_1 */

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(LEDBP_GPIO_Port, LEDBP_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB, R_W_Pin|EN_Pin|D4_Pin|D5_Pin
                          |D6_Pin|D7_Pin|RS_Pin, GPIO_PIN_RESET);

  /*Configure GPIO pin : LEDBP_Pin */
  GPIO_InitStruct.Pin = LEDBP_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(LEDBP_GPIO_Port, &GPIO_InitStruct);

  /*Configure GPIO pins : P1_0_Pin P1_1_Pin P1_2_Pin P1_3_Pin
                           P1_4_Pin P1_5_Pin P1_6_Pin P1_7_Pin */
  GPIO_InitStruct.Pin = P1_0_Pin|P1_1_Pin|P1_2_Pin|P1_3_Pin
                          |P1_4_Pin|P1_5_Pin|P1_6_Pin|P1_7_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /*Configure GPIO pins : P2_0_Pin P2_6_Pin BOOT1_Pin P2_3_Pin
                           P2_1_Pin P2_2_Pin P2_5_Pin P2_4_Pin
                           P2_7_Pin */
  GPIO_InitStruct.Pin = P2_0_Pin|P2_6_Pin|BOOT1_Pin|P2_3_Pin
                          |P2_1_Pin|P2_2_Pin|P2_5_Pin|P2_4_Pin
                          |P2_7_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

  /*Configure GPIO pins : R_W_Pin EN_Pin D4_Pin D5_Pin
                           D6_Pin D7_Pin RS_Pin */
  GPIO_InitStruct.Pin = R_W_Pin|EN_Pin|D4_Pin|D5_Pin
                          |D6_Pin|D7_Pin|RS_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

/* USER CODE BEGIN MX_GPIO_Init_2 */
/* USER CODE END MX_GPIO_Init_2 */
}

/* USER CODE BEGIN 4 */

//*******************************************************************
//    Nom de la fonction : factoriel
//    Auteur : Yunis Sebany
//    Date de cr�ation : 13-02-26
//    Date de la derni�re modification : 13-02-26
//    Description : Donne la factoriel du nombre en entree
//                 
//    Prototype:     int factoriel(unsigned int uiNumber)                       
//
//    Appel :           factoriel(5) return -> 120                    
//
//    Fonctions appel�es : Aucun
//    Param�tres d'entr�e : iNumber
//    Param�tres de sortie : 	iResult	
//    Variables utilis�es : iResult, iNumber, i
// 	
//******************************************************************
unsigned int factoriel(unsigned int uiNumber)
{

  unsigned int uiResult = 1;
  for (unsigned int i = 1; i <= uiNumber; i++){
    uiResult *= i;
  }
  return uiResult;
}

//*******************************************************************
//    Nom de la fonction : msDelay
//    Auteur : Yunis Sebany
//    Date de cr�ation : 13-02-26
//    Date de la derni�re modification : 13-02-26
//    Description : Delai en ms
//                 
//    Prototype:     void msDelay(unsigned int uiDelay)                     
//
//    Appel :           msDelay(5)                   
//
//    Fonctions appel�es : Aucun
//    Param�tres d'entr�e : uiDelay
//    Param�tres de sortie : 	Aucun
//    Variables utilis�es : uiOut, uiIn,
// 	
//******************************************************************
void msDelay(unsigned int uiDelay){
  for (int i = 0; i < uiDelay; i++){
    for(int j = 0; j < 5200; j++){
      //
    }
  }
}


/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
