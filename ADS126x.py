class Ads126x():
    def __init__(self, x):

        if x == 2:
            self.ADS126x_NUM_REG 	= 0x15		#  ADS1262 has 21 registers */
        if  x == 3:
            self.ADS126x_NUM_REG 	= 0x1B		#  ADS1263 has 27 registers */

#  SPI Commands */
        self.NOP			= 0x00		#  ID/CFG REGISTER (ADDRESS 00h */
        self.RESET			= 0x06		#  ID/CFG REGISTER (ADDRESS 00h */
        self.START1			= 0x08		#  ID/CFG REGISTER (ADDRESS 00h */
        self.STOP1			= 0x0B		#  ID/CFG REGISTER (ADDRESS 00h */
        self.RDATA1			= 0x12		#  ID/CFG REGISTER (ADDRESS 00h */
        self.SYOCAL1		= 0x16		#  ID/CFG REGISTER (ADDRESS 00h */
        self.SYGCAL1		= 0x17		#  ID/CFG REGISTER (ADDRESS 00h */
        self.SFOCAL1		= 0x19		#  ID/CFG REGISTER (ADDRESS 00h */
# Multi-Byte Commands
        self.RREG		    = 0x20		#  ID/CFG REGISTER (ADDRESS 00h */
        self.WREG			= 0x40		#  ID/CFG REGISTER (ADDRESS 00h */
#  Additional ADS1263 Commands */
        if  x == 3:
            self.START2			= 0x0C		#  ID/CFG REGISTER (ADDRESS 00h */
            self.STOP2			= 0x0E		#  ID/CFG REGISTER (ADDRESS 00h */
            self.RDATA2			= 0x14		#  ID/CFG REGISTER (ADDRESS 00h */
            self.SYOCAL2		= 0x1B		#  ID/CFG REGISTER (ADDRESS 00h */
            self.SYGCAL2		= 0x1C		#  ID/CFG REGISTER (ADDRESS 00h */
            self.SFOCAL2		= 0x1E		#  ID/CFG REGISTER (ADDRESS 00h */

#  STATUS Byte Masks */
        #define	ADC2_NEW	= 0x80		#  Indicates new ADC2 data */
        #define	ADC1_NEW	= 0x40		#  Indicates new ADC1 data */
        #define	EXTCLK		= 0x20		#  Indicates ADC clock source */
        #define	REF_ALM		= 0x10		#  Low Reference Alarm   - Only used with ADC1 */
        #define	PGAL_ALM	= 0x08		#  PGA Output Low Alarm  - Only used with ADC1 */
        #define	PGAH_ALM	= 0x04		#  PGA Output High Alarm - Only used with ADC1 */
        #define	PGAD_ALM	= 0x02		#  PGA Diff Output Alarm - Only used with ADC1 */
        #define	RST_ALM		= 0x01		#  Indicates device reset (re-named to avoid conflict */


    #  Register Addresses */
        self.ID				= 0x00		#  ID/CFG REGISTER (ADDRESS 00h */
        self.POWER 			= 0x01		#  CONFIGURATION REGISTER 0 (ADDRESS 01h */
        self.INTERFACE		= 0x02		#  CONFIGURATION REGISTER 1 (ADDRESS 02h */
        self.MODE0			= 0x03		#  High-Pass Filter Corner Frequency, Low Byte (Address 03h */
        self.MODE1			= 0x04		#  High-Pass Filter Corner Frequency, High Byte (Address 04h */
        self.MODE2			= 0x05
        self.INPMUX			= 0x06
        self.OFCAL0			= 0x07
        self.OFCAL1			= 0x08 		#  Offset Calibration, Low Byte (Address 05h */
        self.OFCAL2			= 0x09 		#  Offset Calibration, Mid Byte (Address 06h */
        self.FSCAL0			= 0x0A		#  Offset Calibration, High Byte (Address 07h */ 		#  Full-Scale Calibration, Low Byte (Address 08h */
        self.FSCAL1			= 0x0B		#  Full-Scale Calibration, Mid Byte (Address 09h */
        self.FSCAL2			= 0x0C		#  Full-Scale Calibration, High Byte (Address 0Ah */
        self.IDACMUX		= 0x0D
        self.IDACMAG		= 0x0E
        self.REFMUX			= 0x0F
        self.TDACP			= 0x10
        self.TDACN			= 0x11
        self.GPIOCON		= 0x12
        self.GPIODIR		= 0x13
        self.GPIODAT		= 0x14
        #  Additional ADS1263 Registers */
        # ifdef ADS1263
        self.ADC2CFG		= 0x15
        self.ADC2MUX		= 0x16
        self.ADC2OFC0		= 0x17
        self.ADC2OFC1		= 0x18
        self.ADC2FSC0		= 0x19
        self.ADC2FSC1		= 0x1A
        # endif #  ADS1263 */


    #  Default Register Values */
    # 	self.ID_DEFAULT_VALUE	    	= 0x00		#  ID/CFG REGISTER (ADDRESS 00h*/
        self.POWER_DEFAULT_VALUE		= 0x19		#  CONFIGURATION REGISTER 0 (ADDRESS 01h */
        self.INTERFACE_DEFAULT_VALUE	= 0x05		#  CONFIGURATION REGISTER 1 (ADDRESS 02h */
        self.MODE0_DEFAULT_VALUE		= 0x00		#  High-Pass Filter Corner Frequency, Low Byte (Address 03h */
        self.MODE1_DEFAULT_VALUE		= 0x80		#  High-Pass Filter Corner Frequency, High Byte (Address 04h */
        self.MODE2_DEFAULT_VALUE		= 0x04		#  Offset Calibration, Low Byte (Address 05h */
        self.INPMUX_DEFAULT_VALUE	    = 0x01		#  Offset Calibration, Mid Byte (Address 06h */
        self.OFCAL0_DEFAULT_VALUE	    = 0x00		#  Offset Calibration, High Byte (Address 07h */
        self.OFCAL1_DEFAULT_VALUE	    = 0x00		#  Full-Scale Calibration, Low Byte (Address 08h */
        self.OFCAL2_DEFAULT_VALUE	    = 0x00		#  Full-Scale Calibration, Mid Byte (Address 09h */
        self.FSCAL0_DEFAULT_VALUE   	= 0x00		#  Full-Scale Calibration, High Byte (Address 0Ah */
        self.FSCAL1_DEFAULT_VALUE   	= 0x00
        self.FSCAL2_DEFAULT_VALUE   	= 0x40
        self.IDACMUX_DEFAULT_VALUE	    = 0xBB
        self.IDACMAG_DEFAULT_VALUE	    = 0x00
        self.REFMUX_DEFAULT_VALUE	    = 0x00
        self.TDACP_DEFAULT_VALUE		= 0x00
        self.TDACN_DEFAULT_VALUE		= 0x00
        self.GPIOCON_DEFAULT_VALUE	    = 0x00
        self.GPIODIR_DEFAULT_VALUE	    = 0x00
        self.GPIODAT_DEFAULT_VALUE	    = 0x00

        #ifdef ADS1263
        self.ADC2CFG_DEFAULT_VALUE	    = 0x00
        self.ADC2MUX_DEFAULT_VALUE	    = 0x01
        self.ADC2OFC0_DEFAULT_VALUE	    = 0x00
        self.ADC2OFC1_DEFAULT_VALUE	    = 0x00
        self.ADC2FSC0_DEFAULT_VALUE	    = 0x00
        self.ADC2FSC1_DEFAULT_VALUE	    = 0x40
        #endif #  ADS1263 */


    #  Register Field Definitions */

        #  POWER Register Fields */
        self.RST 				= 0x10
        self.VBIAS 				= 0x02
        self.INTREF 			= 0x01

        #  INTERFACE Register Fields */
        self.TIMEOUT 			= 0x08
        self.STATUS 			= 0x04
    # 	self.CRC1 				= 0x02
    # 	self.CRC0 				= 0x01
        self.CRC_MASK			= 0x03
    # CRC Field
        self.CRC_OFF			= 0x00
        self.CRC_CHKSUM			= 0x01
        self.CRC_ON				= 0x02

        #  MODE0 Register Fields */
        self.REFREV				= 0x80
        self.RUNMODE			= 0x40
    # 	self.CHOP1 				= 0x20
    # 	self.CHOP0 				= 0x10
        self.CHOP_MASK			= 0x30
        # CHOP Field
        self.CHOP_OFF			= 0x00
        self.CHOP_ON			= 0x10
        self.CHOP_IDAC			= 0x20
        self.CHOP_ON_IDAC		= 0x30
    #   self.DELAY3 			= 0x08
    #   self.DELAY2 			= 0x04
    #   self.DELAY1 			= 0x02
    #   self.DELAY0 			= 0x01
        self.DELAY_MASK			= 0x0F		#  Additional Settling Delay Field */
        # DELAY Field
        self.DELAY_0us			= 0x00
        self.DELAY_8_7us		= 0x01
        self.DELAY_17us			= 0x02
        self.DELAY_35us			= 0x03
        self.DELAY_69us			= 0x04
        self.DELAY_139us		= 0x05
        self.DELAY_278us		= 0x06
        self.DELAY_555us		= 0x07
        self.DELAY_1100us		= 0x08
        self.DELAY_2200us		= 0x09
        self.DELAY_4400us		= 0x0A
        self.DELAY_8800us		= 0x0B

    #   MODE1 Register Fields */
    # 	self.FILTER_2 			= 0x80
    # 	self.FILTER_1 			= 0x40
    # 	self.FILTER_0 			= 0x20
        self.FILTER_MASK		= 0xE0
        # DELAY Field
        self.FILTER_SINC1		= 0x00
        self.FILTER_SINC2		= 0x20
        self.FILTER_SINC3		= 0x40
        self.FILTER_SINC4		= 0x60
        self.FILTER_FIR			= 0x80
        self.SBADC 				= 0x10
        self.SBPOL 				= 0x08
    #	self.SBMAG2 			= 0x04
    # 	self.SBMAG1 			= 0x02
    # 	self.SBMAG0 			= 0x01
        self.SBMAG_MASK			= 0x07
                # SBMAG Field
        self.SBMAG_0uA			= 0x00
        self.SBMAG_0_5uA		= 0x01
        self.SBMAG_2uA			= 0x02
        self.SBMAG_10uA			= 0x03
        self.SBMAG_50uA			= 0x04
        self.SBMAG_200uA		= 0x05
        self.SBMAG_10MOhm		= 0x06

        #  MODE2 Register Fields */
        self.BYPASS				= 0x80
    #	self.GAIN2 				= 0x40
    #	self.GAIN1 				= 0x20
    #	self.GAIN0 				= 0x10
        self.GAIN_MASK			= 0x70
    # GAIN Field
        self.GAIN_1				= 0x00
        self.GAIN_2				= 0x10
        self.GAIN_4				= 0x20
        self.GAIN_8				= 0x30
        self.GAIN_16			= 0x40
        self.GAIN_32			= 0x50
    # 	self.DR3 				= 0x08
    # 	self.DR2 				= 0x04
    # 	self.DR1 				= 0x02
    # 	self.DR0 				= 0x01
        self.DR_MASK				= 0x0F
    # DR Field
        self.DR_2_5_SPS			= 0x00
        self.DR_5_SPS			= 0x01
        self.DR_10_SPS			= 0x02
        self.DR_16_6_SPS		= 0x03
        self.DR_20_SPS			= 0x04
        self.DR_50_SPS			= 0x05
        self.DR_60_SPS			= 0x06
        self.DR_100_SPS			= 0x07
        self.DR_400_SPS			= 0x08
        self.DR_1200_SPS		= 0x09
        self.DR_2400_SPS		= 0x0A
        self.DR_4800_SPS		= 0x0B
        self.DR_7200_SPS		= 0x0C
        self.DR_14400_SPS		= 0x0D
        self.DR_19200_SPS		= 0x0E
        self.DR_38400_SPS		= 0x0F


    #   INPMUX Register Fields */
    # 	self.MUXP_3 			= 0x80
    # 	self.MUXP_2 			= 0x40
    # 	self.MUXP_1 			= 0x20
    # 	self.MUXP_0 			= 0x10
        self.MUXP_MASK			= 0xF0
        # MUXP Field
        self.MUXP_AIN0			= 0x00
        self.MUXP_AIN1			= 0x10
        self.MUXP_AIN2			= 0x20
        self.MUXP_AIN3			= 0x30
        self.MUXP_AIN4			= 0x40
        self.MUXP_AIN5			= 0x50
        self.MUXP_AIN6			= 0x60
        self.MUXP_AIN7			= 0x70
        self.MUXP_AIN8			= 0x80
        self.MUXP_AIN9			= 0x90
        self.MUXP_AINCOM		= 0xA0
        self.MUXP_TEMP			= 0xB0
        self.MUXP_AVDD			= 0xC0
        self.MUXP_DVDD			= 0xD0
        self.MUXP_TEST			= 0xE0
        self.MUXP_NO_CONN		= 0xF0
    # 	self.MUXN_3 			= 0x08
    # 	self.MUXN_2 			= 0x04
    # 	self.MUXN_1 			= 0x02
    # 	self.MUXN_0 			= 0x01
        self.MUXN_MASK			= 0x0F
    #   MUXN Field
        self.MUXN_AIN0			= 0x00
        self.MUXN_AIN1			= 0x01
        self.MUXN_AIN2			= 0x02
        self.MUXN_AIN3			= 0x03
        self.MUXN_AIN4			= 0x04
        self.MUXN_AIN5			= 0x05
        self.MUXN_AIN6			= 0x06
        self.MUXN_AIN7			= 0x07
        self.MUXN_AIN8			= 0x08
        self.MUXN_AIN9			= 0x09
        self.MUXN_AINCOM		= 0x0A
        self.MUXN_TEMP			= 0x0B
        self.MUXN_AVSS			= 0x0C
        self.MUXN_DVDD			= 0x0D
        self.MUXN_TEST			= 0x0E
        self.MUXN_NO_CONN		= 0x0F

    #   SKIP OFFSET & GAIN CAL REGISTERS

    #   IDACMUX Register Fields */
    # 	self.MUX2_3 			= 0x80
    # 	self.MUX2_2 			= 0x40
    # 	self.MUX2_1  			= 0x20
    # 	self.MUX2_0 			= 0x10
        self.MUX2_MASK			= 0xF0
    #   MUX2 Field
        self.MUX2_AIN0			= 0x00
        self.MUX2_AIN1			= 0x10
        self.MUX2_AIN2			= 0x20
        self.MUX2_AIN3			= 0x30
        self.MUX2_AIN4			= 0x40
        self.MUX2_AIN5			= 0x50
        self.MUX2_AIN6			= 0x60
        self.MUX2_AIN7			= 0x70
        self.MUX2_AIN8			= 0x80
        self.MUX2_AIN9			= 0x90
        self.MUX2_AINCOM		= 0xA0
        self.MUX2_NO_CONM		= 0xB0
    # 	self.MUX1_3 			= 0x08
    # 	self.MUX1_2 			= 0x04
    # 	self.MUX1_1 			= 0x02
    # 	self.MUX1_0 			= 0x01
        self.MUX1_MASK			= 0x0F
        # MUX1 Field
        self.MUX1_AIN0			= 0x00
        self.MUX1_AIN1			= 0x01
        self.MUX1_AIN2			= 0x02
        self.MUX1_AIN3			= 0x03
        self.MUX1_AIN4			= 0x04
        self.MUX1_AIN5			= 0x05
        self.MUX1_AIN6			= 0x06
        self.MUX1_AIN7			= 0x07
        self.MUX1_AIN8			= 0x08
        self.MUX1_AIN9			= 0x09
        self.MUX1_AINCOM		= 0x0A
        self.MUX1_NO_CONM		= 0x0B

    #   IDACMAG Register Fields */
    # 	self.MAG2_3 			= 0x80
    # 	self.MAG2_2 			= 0x40
    # 	self.MAG2_1 			= 0x20
    # 	self.MAG2_0 			= 0x10
        self.MAG2_MASK			= 0xF0
        # MAG2 Field
        self.MAG2_OFF			= 0x00
        self.MAG2_50uA			= 0x10
        self.MAG2_100uA			= 0x20
        self.MAG2_250uA			= 0x30
        self.MAG2_500uA			= 0x40
        self.MAG2_750uA			= 0x50
        self.MAG2_1000uA		= 0x60
        self.MAG2_1500uA		= 0x70
        self.MAG2_2000uA		= 0x80
        self.MAG2_2500uA		= 0x90
        self.MAG2_3000uA		= 0xA0
    # 	self.MAG1_3				= 0x08
    # 	self.MAG1_2 			= 0x04
    # 	self.MAG1_1 			= 0x02
    # 	self.MAG1_0 			= 0x01
        self.MAG1_MASK			= 0xF0
        # MAG1 Field
        self.MAG1_OFF			= 0x00
        self.MAG1_50uA			= 0x01
        self.MAG1_100uA			= 0x02
        self.MAG1_250uA			= 0x03
        self.MAG1_500uA			= 0x04
        self.MAG1_750uA			= 0x05
        self.MAG1_1000uA		= 0x06
        self.MAG1_1500uA		= 0x07
        self.MAG1_2000uA		= 0x08
        self.MAG1_2500uA		= 0x09
        self.MAG1_3000uA		= 0x0A

    #   REFMUX Register Fields */
    # 	self.RMUXP_2	 		= 0x20
    # 	self.RMUXP_1	 		= 0x10
    # 	self.RMUXP_0	 		= 0x08
        self.RMUXP_MASK			= 0x38
        # MUXP Field
        self.RMUXP_INTP			= 0x00
        self.RMUXP_AIN0			= 0x08
        self.RMUXP_AIN2			= 0x10
        self.RMUXP_AIN4			= 0x18
        self.RMUXP_AVDD			= 0x20
    # 	self.RMUXN_2	 		= 0x04
    # 	self.RMUXN_1	 		= 0x02
    # 	self.RMUXN_0	 		= 0x01
        self.RMUXN_MASK			= 0x07
        # MUXN Field
        self.RMUXN_INTN			= 0x00
        self.RMUXN_AIN1			= 0x01
        self.RMUXN_AIN3			= 0x02
        self.RMUXN_AIN5			= 0x03
        self.RMUXN_AVSS			= 0x04

    #   TDACP Register Fields */
        self.OUTP	 				= 0x80
        # OUTP Field
        self.OUTP_NO_CONN	    	= 0x00
        self.OUTP_AIN6		       	= 0x80
    # 	self.MAGP4	 				= 0x10
    # 	self.MAGP3	 				= 0x08
    # 	self.MAGP2	 				= 0x04
    # 	self.MAGP1	 				= 0x02
    # 	self.MAGP0	 				= 0x01
        self.MAGP_MASK				= 0x1F
        # MAGP Field
        self.MAGP_0_9_AVDD		    = 0x09
        self.MAGP_0_7_AVDD		    = 0x08
        self.MAGP_0_6_AVDD		    = 0x07
        self.MAGP_0_55_AVDD		    = 0x06
        self.MAGP_0_525_AVDD	    = 0x05
        self.MAGP_0_5125_AVDD	    = 0x04
        self.MAGP_0_50625_AVDD	    = 0x03
        self.MAGP_0_503125_AVDD	    = 0x02
        self.MAGP_0_5015625_AVDD	= 0x01
        self.MAGP_0_5_AVDD	    	= 0x00
        self.MAGP_0_4984375_AVDD	= 0x11
        self.MAGP_0_496875_AVDD	    = 0x12
        self.MAGP_0_49375_AVDD	    = 0x13
        self.MAGP_0_4875_AVDD	    = 0x14
        self.MAGP_0_475_AVDD		= 0x15
        self.MAGP_0_45_AVDD		    = 0x16
        self.MAGP_0_4_AVDD		    = 0x17
        self.MAGP_0_3_AVDD		    = 0x18
        self.MAGP_0_1_AVDD		    = 0x19

    #   DACN Register Fields */
        self.OUTN	 				= 0x80
        # OUTN Field
        self.OUTN_NO_CONN	    	= 0x00
        self.OUTN_AIN7		    	= 0x80
    # 	self.MAGN4	 				= 0x10
    # 	self.MAGN3	 				= 0x08
    # 	self.MAGN2	 				= 0x04
    # 	self.MAGN1	 				= 0x02
    # 	self.MAGN0	 				= 0x01
        self.MAGN_MASK				= 0x1F
        # MAGN Field
        self.MAGN_0_9_AVSS	    	= 0x09
        self.MAGN_0_7_AVSS	    	= 0x08
        self.MAGN_0_6_AVSS	    	= 0x07
        self.MAGN_0_55_AVSS	    	= 0x06
        self.MAGN_0_525_AVSS		= 0x05
        self.MAGN_0_5125_AVSS   	= 0x04
        self.MAGN_0_50625_AVSS  	= 0x03
        self.MAGN_0_503125_AVSS	    = 0x02
        self.MAGN_0_5015625_AVSS	= 0x01
        self.MAGN_0_5_AVSS		    = 0x00
        self.MAGN_0_4984375_AVSS	= 0x11
        self.MAGN_0_496875_AVSS	    = 0x12
        self.MAGN_0_49375_AVSS  	= 0x13
        self.MAGN_0_4875_AVSS   	= 0x14
        self.MAGN_0_475_AVSS		= 0x15
        self.MAGN_0_45_AVSS	    	= 0x16
        self.MAGN_0_4_AVSS	       	= 0x17
        self.MAGN_0_3_AVSS	    	= 0x18
        self.MAGN_0_1_AVSS	    	= 0x19

    #   GPIOCON Register Fields */
        self.CON7_AINCOM			= 0x80
        self.CON6_AIN09				= 0x40
        self.CON5_AIN08				= 0x20
        self.CON4_AIN07				= 0x10
        self.CON3_AIN06				= 0x08
        self.CON2_AIN05				= 0x04
        self.CON1_AIN04				= 0x02
        self.CON0_AIN03				= 0x01

    #   GPIODIR Register Fields */
        self.DIR7_AINCOM			= 0x80
        self.DIR6_AIN09				= 0x40
        self.DIR5_AIN08				= 0x20
        self.DIR4_AIN07				= 0x10
        self.DIR3_AIN06				= 0x08
        self.DIR2_AIN05				= 0x04
        self.DIR1_AIN04				= 0x02
        self.DIR0_AIN03				= 0x01

    #   GPIODAT Register Fields */
        self.DAT7_AINCOM			= 0x80
        self.DAT6_AIN09				= 0x40
        self.DAT5_AIN08				= 0x20
        self.DAT4_AIN07				= 0x10
        self.DAT3_AIN06				= 0x08
        self.DAT2_AIN05				= 0x04
        self.DAT1_AIN04				= 0x02
        self.DAT0_AIN03				= 0x01


    #  Additional ADS1263 Registers */
    #ifdef ADS1263

    #   ADC2CFG Register Fields */
    # 	self.DR2_1	 	= 0x80
    # 	self.DR2_0	 	= 0x40
        self.DR2_MASK			= 0xC0
        # DR_2 Field
        self.DR2_10SPS	= 0x00
        self.DR2_100SPS	= 0x40
        self.DR2_400SPS	= 0x80
        self.DR2_800SPS	= 0xC0
    # 	self.REF2_2	 	= 0x20
    # 	self.REF2_1		= 0x10
    # 	self.REF2_0	 	= 0x08
        self.REF2_MASK			= 0x38
    #   REF2 Field
        self.REF2_INTP_INTN= 0x00
        self.REF2_AIN0_AIN1= 0x08
        self.REF2_AIN2_AIN3= 0x10
        self.REF2_AIN4_AIN5= 0x18
        self.REF2_AVDD_AVSS= 0x38
    # 	self.GAIN2_2	 	= 0x04
    # 	self.GAIN2_1		= 0x02
    # 	self.GAIN2_0		= 0x01
        self.GAIN2_MASK			= 0x07
        # GAIN2 Field
        self.GAIN2_1		= 0x00
        self.GAIN2_2		= 0x01
        self.GAIN2_4		= 0x02
        self.GAIN2_8		= 0x03
        self.GAIN2_16	= 0x04
        self.GAIN2_32	= 0x05
        self.GAIN2_64	= 0x06
        self.GAIN2_128	= 0x07


    #   DC2MUX Register Fields */
    # 	self.MUXP2_3	 	= 0x80
    # 	self.MUXP2_2	 	= 0x40
    # 	self.MUXP2_1	 	= 0x20
    # 	self.MUXP2_0		= 0x10
        self.MUXP2_MASK		= 0xF0
        # MUXP2 Field
        self.MUXP2_AIN0	= 0x00
        self.MUXP2_AIN1	= 0x10
        self.MUXP2_AIN2	= 0x20
        self.MUXP2_AIN3	= 0x30
        self.MUXP2_AIN4	= 0x40
        self.MUXP2_AIN5	= 0x50
        self.MUXP2_AIN6	= 0x60
        self.MUXP2_AIN7	= 0x70
        self.MUXP2_AIN8	= 0x80
        self.MUXP2_AIN9	= 0x90
        self.MUXP2_AINCOM= 0xA0
        self.MUXP2_TEMP	= 0xB0
        self.MUXP2_AVDD	= 0xC0
        self.MUXP2_DVDD	= 0xD0
        self.MUXP2_TEST	= 0xE0
        self.MUXP2_NO_CONN= 0xF0
    # 	self.MUXN2_3	 	= 0x08
    # 	self.MUXN2_2	 	= 0x04
    # 	self.MUXN2_1		= 0x02
    # 	self.MUXN2_0		= 0x01
        self.MUXN2_MASK		= 0x0F
        # MUXN2 Field
        self.MUXN2_AIN0	= 0x00
        self.MUXN2_AIN1	= 0x01
        self.MUXN2_AIN2	= 0x02
        self.MUXN2_AIN3	= 0x03
        self.MUXN2_AIN4	= 0x04
        self.MUXN2_AIN5	= 0x05
        self.MUXN2_AIN6	= 0x06
        self.MUXN2_AIN7	= 0x07
        self.MUXN2_AIN8	= 0x08
        self.MUXN2_AIN9	= 0x09
        self.MUXN2_AINCOM= 0x0A
        self.MUXN2_TEMP	= 0x0B
        self.MUXN2_AVSS	= 0x0C
        self.MUXN2_DVDD	= 0x0D
        self.MUXN2_TEST	= 0x0E
        self.MUXN2_NO_CONN= 0x0F

				# SKIP ADC2 OFFSET & GAIN CAL REGISTERS

		#endif #  ADS1263 */

# END ADC DEFINITIONS


#  Function Prototypes */

	# Low level

	void set_adc_CS(uint8_t state;						# CS pin control
	void set_adc_START(uint8_t state;					# START pin control
	unsigned char ADS126xXferByte (unsigned char cData;	# receive byte, simultaneously send data - this function realizes all
															# necessary functionality, the other Send/Receive methods are only
															# designed to improve readability of the code


	# Higher level

	int32_t ADS126xReadData(uint8_t NumBytes, uint8_t DataByteStartNum;

# int32_t ADS126xREADandWRITE(int NumDatBytes, int StartAddress, int NumRegs, unsigned char * pdata;
# unsigned char ADS126xReadADC2Data(bufferType_t *readbuffer;

# read a number of consecutive registers to a given array pointer
void ADS126xReadRegister(int StartAddress, int NumRegs, unsigned char *pdata;

# write a number of consecutive registers from a given array pointer
void ADS126xWriteRegister(int StartAddress, int NumRegs, unsigned char *pdata;

# Reset by command (alternative to pin
void ADS126xSendResetCommand(void;

# Start by command (alternative to pin
void ADS126xSendStartCommand(void;

void ADS126xSendStopCommand(void;
void ADS126xSendADC2StartCommand(void;
void ADS126xSendADC2StopCommand(void;



#endif #  ADS126X_H_ */